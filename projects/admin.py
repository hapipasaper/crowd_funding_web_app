from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Project, ProjectImage, Donation


# ✅ Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# ✅ Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# ✅ Inlines for Project
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class DonationInline(admin.TabularInline):
    model = Donation
    extra = 0
    readonly_fields = ("user", "amount", "created_at")


# ✅ Project
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "creator",
        "created_at",
        "safe_total_donations",
        "safe_progress",
        "safe_average_rating",
        "is_canceled",
        "safe_thumbnail",
    )
    list_filter = ("category", "created_at", "is_canceled")
    search_fields = ("title", "details", "creator__username")
    inlines = [ProjectImageInline, DonationInline]

    # ✅ Average Rating (always returns str)
    def safe_average_rating(self, obj):
        try:
            ratings = obj.ratings.all()
            if ratings.exists():
                avg = sum(r.stars for r in ratings) / ratings.count()
                return str(round(avg, 2))
            return "-"
        except Exception as e:
            return f"ERR: {e}"
    safe_average_rating.short_description = "Avg Rating"

    # ✅ Total Donations (always returns str)
    def safe_total_donations(self, obj):
        try:
            total = sum(float(d.amount or 0) for d in obj.donations.all())
            return str(round(total, 2))
        except Exception as e:
            return f"ERR: {e}"
    safe_total_donations.short_description = "Total Donations"

    # ✅ Progress (always returns str)
    def safe_progress(self, obj):
        try:
            if obj.target and float(obj.target) > 0:
                total = sum(float(d.amount or 0) for d in obj.donations.all())
                percent = (total / float(obj.target)) * 100
                return f"{percent:.2f}%"
            return "0%"
        except Exception as e:
            return f"ERR: {e}"
    safe_progress.short_description = "Progress"

    # ✅ Thumbnail (always returns str)
    def safe_thumbnail(self, obj):
        try:
            first_image = obj.images.first()
            if first_image:
                return format_html(
                    '<img src="{}" style="width:60px; height:40px; object-fit:cover;" />',
                    first_image.image.url,
                )
            return "-"
        except Exception as e:
            return f"ERR: {e}"
    safe_thumbnail.short_description = "Image"
    # ✅ Donation
@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "amount", "created_at")
    list_filter = ("created_at", "project")
    search_fields = ("project_title", "user_username")