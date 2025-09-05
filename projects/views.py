from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum,Avg
from .models import Project, ProjectImage, Rating, Tag, Donation
from .forms import ProjectForm, DonationForm, CommentForm, RatingForm
from django.db import models
from django.db.models import Q

# 🟢 إنشاء مشروع جديد
@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        images = request.FILES.getlist("images")  # لو فيه صور متعددة

        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()

            # ✅ حفظ التاجز
            tags_input = form.cleaned_data.get("tags")
            if tags_input:
                tags_list = [t.strip() for t in tags_input.split(",")]
                for tag_name in tags_list:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    project.tags.add(tag)

            # ✅ حفظ الصور
            for img in images:
                ProjectImage.objects.create(project=project, image=img)

            messages.success(request, "Project created successfully!")
            return redirect("projects:project_detail", pk=project.pk)
    else:
        form = ProjectForm()

    return render(request, "projects/project_form.html", {"form": form})


# 🟢 تفاصيل المشروع + التبرعات + المشاريع المشابهة
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # ✅ حساب التبرعات والتقدم
    total_donations = project.donations.aggregate(total=Sum("amount"))["total"] or 0
    progress = int((total_donations / project.target) * 100) if project.target > 0 else 0

    # ✅ Forms
    donation_form = DonationForm()
    comment_form = CommentForm()
    rating_form = RatingForm()

    if request.method == "POST":
        if "donate" in request.POST:
            donation_form = DonationForm(request.POST)
            if donation_form.is_valid():
                donation = donation_form.save(commit=False)
                donation.project = project
                donation.user = request.user
                donation.save()
                messages.success(request, "Donation added successfully!")
                return redirect("projects:project_detail", pk=project.pk)

        elif "comment_submit" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                parent_id = request.POST.get("parent_id")
                comment = comment_form.save(commit=False)
                comment.project = project
                comment.user = request.user
                if parent_id:
                    comment.parent_id = parent_id
                comment.save()
                messages.success(request, "Comment added successfully!")
                return redirect("projects:project_detail", pk=project.pk)

        elif "rating_submit" in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating, created = Rating.objects.update_or_create(
                    project=project,
                    user=request.user,
                    defaults={"stars": rating_form.cleaned_data["stars"]},
                )
                messages.success(request, "Rating submitted successfully!")
                return redirect("projects:project_detail", pk=project.pk)

    # ✅ حساب متوسط التقييم
    avg_rating = project.ratings.aggregate(avg=models.Avg("stars"))["avg"] or 0

    # ✅ المشاريع المشابهة
    similar_projects = Project.objects.filter(
        tags__in=project.tags.all()
    ).exclude(id=project.id).distinct()[:4]

    return render(request, "projects/project_detail.html", {
        "project": project,
        "donation_form": donation_form,
        "comment_form": comment_form,
        "rating_form": rating_form,
        "total_donations": total_donations,
        "progress": progress,
        "avg_rating": avg_rating,
        "similar_projects": similar_projects,
    })
# 🟢 إلغاء المشروع
@login_required
def cancel_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # ✅ حساب نسبة التبرعات
    total_donations = project.donations.aggregate(total=Sum("amount"))["total"] or 0
    progress = (total_donations / project.target) * 100 if project.target > 0 else 0

    if progress < 25:  # ينفع يتلغي لو أقل من 25%
        project.is_canceled = True
        project.save()
        messages.warning(request, "Project has been canceled.")
    else:
        messages.error(request, "You cannot cancel this project (donations >= 25%).")

    return redirect("projects:project_detail", pk=project.pk)

@login_required
def reports(request):
    projects = Project.objects.all().annotate(
        total_donations=Sum("donations__amount"),
        comments_count=models.Count("comments"),
        avg_rating=models.Avg("ratings__stars"),
    )
    return render(request, "projects/reports.html", {"projects": projects})


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
        "projects": projects,})

def project_search(request):
    query = request.GET.get("q", "")  # لو مفيش query هيرجع string فاضي
    if query:
        projects = Project.objects.filter(title__icontains=query)
    else:
        projects = Project.objects.all()  # ممكن تخليها [] لو مش عاوز كل المشاريع تظهر

    context = {
        "projects": projects,
        "query": query,
    }
    return render(request, "projects/search.html",context)