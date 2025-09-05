from django.shortcuts import render
from projects.models import Project
from django.db.models import Avg

def homepage(request):
    # 🏆 Top 5 rated
    top_rated = Project.objects.annotate(
        avg_rating=Avg("ratings__stars")
    ).order_by("-avg_rating")[:5]

    # 🆕 Latest 5
    latest_projects = Project.objects.order_by("-created_at")[:5]

    # 📂 All
    projects = Project.objects.all().order_by("-created_at")

    return render(request, "core/home.html", {
        "top_rated": top_rated,
        "latest_projects": latest_projects,
        "projects": projects,
    })