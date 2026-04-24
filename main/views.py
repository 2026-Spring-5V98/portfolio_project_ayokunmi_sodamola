import json
import time

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from . import chatbot
from .forms import ContactForm
from .projects_data import PROJECTS, PROJECTS_BY_SLUG


def home(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print("[Contact form submission]", form.cleaned_data)
            messages.success(request, "Thanks — your message has been received.")
            return redirect(request.path + "#contact")

    return render(request, "main/home.html", {
        "projects": PROJECTS,
        "form": form,
    })


def about_me(request):
    return render(request, "main/about_me.html")


def project_detail(request, slug):
    project = PROJECTS_BY_SLUG.get(slug)
    if not project:
        raise Http404("Project not found")
    return render(request, "main/project_detail.html", {"project": project})


def not_found(request, exception=None):
    return render(request, "main/404.html", status=404)


@require_POST
def chat(request):
    if not settings.GEMINI_API_KEY:
        return JsonResponse(
            {"error": "Chat is not configured yet. Please try again later."},
            status=503,
        )

    ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "anon"))
    ip = ip.split(",")[0].strip()
    bucket_key = f"chat:rate:{ip}:{int(time.time() // 60)}"
    hits = cache.get(bucket_key, 0)
    if hits >= 15:
        return JsonResponse({"error": "Too many messages. Slow down a bit."}, status=429)
    cache.set(bucket_key, hits + 1, timeout=70)

    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    message = (payload.get("message") or "").strip()
    if not message:
        return JsonResponse({"error": "Message is required."}, status=400)
    if len(message) > 1000:
        return JsonResponse({"error": "Message is too long (max 1000 chars)."}, status=400)

    try:
        reply = chatbot.get_reply(message)
    except Exception as exc:
        print("[chat] error:", exc)
        return JsonResponse({"error": "Something went wrong. Please try again."}, status=500)

    return JsonResponse({"reply": reply or "I'm not sure how to answer that."})
