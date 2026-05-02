from django.db import models


class Project(models.Model):
    """A portfolio project. Field names align with the AI Principles rubric:
    title, summary, description, category, tools_used, challenges, lessons_learned, image, links.
    """

    # Identity
    slug = models.SlugField(max_length=80, unique=True)
    title = models.CharField(max_length=120)
    detail_title = models.CharField(max_length=200, blank=True)

    # Card + hero copy
    summary = models.TextField(help_text="Short description shown on the homepage card.")
    description = models.TextField(
        blank=True,
        help_text="Long-form overview shown on the detail page (used by professional projects).",
    )
    one_sentence_summary = models.CharField(
        max_length=400,
        blank=True,
        help_text="One-sentence hero subtitle. When set, the detail page renders the 8-section student layout.",
    )

    # Meta
    category = models.CharField(max_length=200, help_text="e.g. 'Fintech, Banking, Enterprise'.")
    role = models.CharField(max_length=120)
    company = models.CharField(max_length=120)

    # Stack + outcomes (lists stored as JSON)
    tools_used = models.JSONField(default=list, help_text="List of tool/tech names rendered as chips.")
    challenges = models.JSONField(default=list, blank=True, help_text="Bullet list (professional layout).")
    solutions = models.JSONField(default=list, blank=True, help_text="Bullet list (professional layout).")
    impact = models.JSONField(default=list, blank=True, help_text="Bullet list (professional layout).")
    key_features = models.JSONField(default=list, blank=True, help_text="Bullet list (student layout).")

    # Student-layout paragraphs
    business_problem = models.TextField(blank=True)
    role_contribution = models.TextField(blank=True)
    biggest_challenge = models.TextField(blank=True)
    lessons_learned = models.TextField(blank=True, help_text="Rendered as 'What I Learned' on student detail pages.")

    # Asset + links
    image = models.CharField(max_length=200, help_text="Filename inside main/static/main/images/.")
    live_url = models.URLField(blank=True)
    try_it_url = models.URLField(blank=True)

    # Ordering
    display_order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.title


class Skill(models.Model):
    """A single skill/tool tag rendered in the homepage Skills section."""

    GROUP_CHOICES = [
        ("core", "Core Competencies"),
        ("languages", "Programming Languages"),
        ("tools", "Technologies & Tools"),
    ]

    name = models.CharField(max_length=80)
    group = models.CharField(max_length=20, choices=GROUP_CHOICES)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["group", "display_order", "id"]

    def __str__(self):
        return f"{self.name} ({self.get_group_display()})"


class Experience(models.Model):
    """A single role in the professional experience timeline."""

    title = models.CharField(max_length=120)
    company = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.CharField(max_length=40, help_text="Free-form, e.g. 'Feb 2025'.")
    end_date = models.CharField(max_length=40, help_text="Free-form, e.g. 'Present'.")
    bullets = models.JSONField(default=list, help_text="List of accomplishment bullets.")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.title} at {self.company}" 
