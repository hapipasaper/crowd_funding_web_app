from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


# ✅ Category (تصنيف المشروع)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ✅ Tag (وسوم المشروع)
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# ✅ Project (المشروع نفسه)
class Project(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="projects")
    target = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    is_canceled = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # ✅ مجموع التبرعات
    def get_total_donations(self):
        return float(sum(float(d.amount or 0) for d in self.donations.all()))

    # ✅ نسبة الإنجاز
    def get_progress_percent(self):
        total = self.get_total_donations()
        return (total / float(self.target) * 100) if float(self.target) > 0 else 0.0


# ✅ ProjectImage (صور المشروع)
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="project_images/")

    def __str__(self):
        return f"Image for {self.project.title}"


# ✅ Donation (تبرعات)
class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="donations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} donated {self.amount} to {self.project.title}"


# ✅ Comment
class Comment(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.project}"


# ✅ Rating
class Rating(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(default=1)  # 1 to 5

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.stars}⭐ by {self.user} on {self.project}"


# ✅ Report
class Report(models.Model):
    REPORT_CHOICES = (
        ("project", "Project"),
        ("comment", "Comment"),
    )
    report_type = models.CharField(max_length=20, choices=REPORT_CHOICES)
    project = models.ForeignKey("Project", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.user} on {self.report_type}"