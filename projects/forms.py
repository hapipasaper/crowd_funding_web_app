from django import forms
from .models import Project, Donation, Tag,Comment, Rating, Report



# ✅ فورم إنشاء مشروع جديد
class ProjectForm(forms.ModelForm):
    # tags هندخلها كـ نص عادي (health, education, charity)
    tags = forms.CharField(
        required=False,
        help_text="Separate tags with commas (مثال: health, education, charity)"
    )

    class Meta:
        model = Project
        fields = ["title", "details", "category", "target", "tags"]

    def save(self, commit=True, creator=None):
        project = super().save(commit=False)
        if creator:
            project.creator = creator
        if commit:
            project.save()

            # ✅ معالجة التاجز
            tags_input = self.cleaned_data.get("tags", "")
            if tags_input:
                tag_names = [t.strip() for t in tags_input.split(",") if t.strip()]
                for name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=name)
                    project.tags.add(tag)

        return project


# ✅ فورم التبرع
class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter amount in EGP"
                }
            )
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Write a comment..."})
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["stars"]
        widgets = {
            "stars": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5})
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["report_type", "reason"]
        widgets = {
            "report_type": forms.Select(attrs={"class": "form-control"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Why are you reporting?"})
        }