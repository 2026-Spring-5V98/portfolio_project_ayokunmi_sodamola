from django.contrib import admin

from .models import Experience, Project, Skill


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("display_order", "title", "company", "category", "slug")
    list_display_links = ("title",)
    list_editable = ("display_order",)
    search_fields = ("title", "company", "category", "slug")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Identity", {"fields": ("display_order", "slug", "title", "detail_title", "image")}),
        ("Card + hero copy", {"fields": ("summary", "description", "one_sentence_summary")}),
        ("Meta", {"fields": ("category", "role", "company")}),
        ("Stack + outcomes (lists)", {
            "fields": ("tools_used", "challenges", "solutions", "impact", "key_features"),
            "description": "Each list field accepts a JSON array, e.g. [\"Django\", \"Python\"].",
        }),
        ("Student-layout paragraphs", {
            "fields": ("business_problem", "role_contribution", "biggest_challenge", "lessons_learned"),
            "description": "Filling in 'one_sentence_summary' switches the detail page to the 8-section student layout.",
        }),
        ("Links", {"fields": ("live_url", "try_it_url")}),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("display_order", "name", "group")
    list_display_links = ("name",)
    list_editable = ("display_order",)
    list_filter = ("group",)
    search_fields = ("name",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("display_order", "title", "company", "start_date", "end_date")
    list_display_links = ("title",)
    list_editable = ("display_order",)
    search_fields = ("title", "company")
