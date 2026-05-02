from django.db import migrations


# Field renames between the legacy static dicts (projects_data.py) and the model.
LEGACY_TO_MODEL = {
    "short_description": "summary",
    "overview": "description",
    "industry": "category",
    "technologies": "tools_used",
    "what_you_learned": "lessons_learned",
}

# Fields the model accepts. Anything else in the legacy dict is dropped.
MODEL_FIELDS = {
    "slug", "title", "detail_title",
    "summary", "description", "one_sentence_summary",
    "category", "role", "company",
    "tools_used", "challenges", "solutions", "impact", "key_features",
    "business_problem", "role_contribution", "biggest_challenge", "lessons_learned",
    "image", "live_url", "try_it_url",
    "display_order",
}


def _map_legacy(d, order):
    out = {"display_order": order}
    for k, v in d.items():
        key = LEGACY_TO_MODEL.get(k, k)
        if key in MODEL_FIELDS:
            out[key] = v
    out.setdefault("description", "")
    out.setdefault("live_url", "")
    out.setdefault("try_it_url", "")
    return out


def seed_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    from main.projects_data import PROJECTS

    for i, p in enumerate(PROJECTS):
        Project.objects.update_or_create(
            slug=p["slug"],
            defaults=_map_legacy(p, i),
        )


def unseed_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    Project.objects.all().delete()


SKILLS = [
    ("core", [
        "Product Discovery", "Product Design", "User Experience", "Agile (SCRUM)",
        "Database Modeling", "AI/ML Product Strategy", "Data Analysis",
        "Machine Learning", "Business Analysis", "Change Management", "Process Optimization",
    ]),
    ("languages", ["Python", "SQL", "R", "JavaScript", "HTML"]),
    ("tools", [
        "Google Analytics", "Jira", "PowerBI", "Excel", "Figma", "Visio",
        "Tableau", "PowerPoint", "MS Project", "Confluence", "Linux",
    ]),
]


def seed_skills(apps, schema_editor):
    Skill = apps.get_model("main", "Skill")
    for group, names in SKILLS:
        for i, name in enumerate(names):
            Skill.objects.update_or_create(
                name=name, group=group,
                defaults={"display_order": i},
            )


def unseed_skills(apps, schema_editor):
    Skill = apps.get_model("main", "Skill")
    Skill.objects.all().delete()


EXPERIENCE = [
    {
        "title": "Research Technology Assistant",
        "company": "Baylor University",
        "location": "Texas, US",
        "start_date": "Feb 2025",
        "end_date": "Present",
        "bullets": [
            "Conducts system maintenance including software updates, node health checks, and hardware troubleshooting.",
            "Monitors CPU/GPU node performance on the Kodiak HPC cluster and escalates anomalies, reducing system downtime by 42%.",
            "Delivers Linux and HPC access training to users, improving self-sufficiency and reducing basic support inquiries by 20%.",
        ],
    },
    {
        "title": "Technical Product Manager",
        "company": "MAX",
        "location": "Texas, US",
        "start_date": "June 2024",
        "end_date": "December 2024",
        "bullets": [
            "Led user feedback sessions and usability studies, driving roadmap prioritization and boosting enterprise subscriptions by 15%.",
            "Led cross-functional delivery across engineering, analytics, and product teams (8 members), resolving platform issues by 70%.",
            "Redesigned the end-to-end vehicle refurbishment customer journey through competitive research, driving a 20% increase in user engagement and CSAT.",
        ],
    },
    {
        "title": "Associate Product Manager",
        "company": "Qore",
        "location": "Manchester, UK",
        "start_date": "April 2022",
        "end_date": "June 2024",
        "bullets": [
            "Led design and implementation of an agentic AI-powered customer support chatbot using ML and automation, resulting in a 10% increase in recurring revenue.",
            "Automated FAQs and routine processes, reducing customer support churn by 40% and saving $50,000 in operational cost.",
            "Coordinated engineering and ML teams to deploy an AI-driven customer support system, improving transaction completion by 19%.",
        ],
    },
    {
        "title": "Program Manager",
        "company": "Leadway",
        "location": "London, UK",
        "start_date": "May 2020",
        "end_date": "April 2022",
        "bullets": [
            "Managed delivery governance for a $2M enterprise program portfolio, aligning engineering, compliance, and operations across workstreams.",
            "Implemented and documented ISO 27001 procedures and performed audits, leading to an 80% reduction in security breaches.",
            "Maintained the RAID log across projects, contributing to a 45% reduction in identified risks and issues.",
            "Executed cross-functional program delivery for Leadway Health, achieving 62,000 enrollees and $6MM revenue in year one.",
        ],
    },
]


def seed_experience(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")
    for i, exp in enumerate(EXPERIENCE):
        Experience.objects.update_or_create(
            title=exp["title"], company=exp["company"],
            defaults={**exp, "display_order": i},
        )


def unseed_experience(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")
    Experience.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_projects, unseed_projects),
        migrations.RunPython(seed_skills, unseed_skills),
        migrations.RunPython(seed_experience, unseed_experience),
    ]
