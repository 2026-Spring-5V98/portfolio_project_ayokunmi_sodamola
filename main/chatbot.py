from functools import lru_cache
from pathlib import Path

from django.conf import settings
from google import genai
from google.genai import types

KNOWLEDGE_PATH = Path(__file__).parent / "chatbot_knowledge.md"

SYSTEM_PROMPT_TEMPLATE = """You are a friendly virtual assistant embedded on Ayokunmi Sodamola's portfolio website. Your job is to help visitors learn about Ayokunmi — his background, skills, and past work. Ayokunmi uses he/him pronouns; always refer to him as "he/him/his".

Rules:
- Answer ONLY from the knowledge base below. Do not invent experience, dates, metrics, or contact details.
- If a question is outside what the knowledge base covers, say you're not sure and suggest the visitor reach out via ayokunmi84@gmail.com or LinkedIn (https://www.linkedin.com/in/ayokunmis).
- Keep replies concise: 1–3 short paragraphs. Friendly and professional. Refer to Ayokunmi in the third person with he/him pronouns.
- If the visitor asks about hiring, availability, or internships — mention he's seeking Summer 2026 opportunities and share his email.

# Knowledge base
{knowledge}
"""


@lru_cache(maxsize=1)
def _system_prompt() -> str:
    return SYSTEM_PROMPT_TEMPLATE.format(knowledge=KNOWLEDGE_PATH.read_text())


@lru_cache(maxsize=1)
def _client() -> genai.Client:
    if not settings.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured")
    return genai.Client(api_key=settings.GEMINI_API_KEY)


def get_reply(user_message: str) -> str:
    response = _client().models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=_system_prompt(),
            temperature=0.6,
            max_output_tokens=500,
        ),
    )
    return (response.text or "").strip()
