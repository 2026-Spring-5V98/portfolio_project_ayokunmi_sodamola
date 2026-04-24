from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about-me/", views.about_me, name="about_me"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("chat/", views.chat, name="chat"),
]
