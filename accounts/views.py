from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm





from .forms import (
    UserRegisterForm,
    EmailAuthenticationForm,
    UserUpdateForm,
    ProfileUpdateForm,
)
from .models import User
from .utils import make_activation_token, validate_activation_token


# ---------------- Profile Views ----------------
@login_required
def profile(request):
    """عرض صفحة البروفايل"""
    return render(request, "accounts/profile.html", {"user": request.user})


@login_required
def edit_profile(request):
    """تعديل بيانات البروفايل"""
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()   # لازم نحفظ البروفايل كمان
            messages.success(request, "تم تحديث البروفايل بنجاح")
            return redirect("accounts:profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(
        request,
        "accounts/edit_profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def delete_account(request):
    """حذف الحساب"""
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "تم حذف الحساب بنجاح.")
        return redirect("core:home")  # غيريها حسب الصفحة الرئيسية عندك
    return redirect("accounts:profile")


# ---------------- Auth Views ----------------
class RegisterView(View):
    """تسجيل مستخدم جديد مع إرسال لينك التفعيل"""
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # يتفعل عن طريق اللينك
            user.save()

            # Generate token & activation url
            token = make_activation_token(user)
            activation_url = settings.SITE_URL + reverse(
                "accounts:activate", args=[token]
            )

            subject = "Activate your account"
            message = (
                f"Hi {user.first_name or user.email},\n\n"
                f"Please activate your account using the link below:\n{activation_url}\n\n"
                "This link will expire in 24 hours.\n\n"
                "Thanks."
            )

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            messages.success(
                request,
                "Registration successful. Check your email for the activation link.",
            )
            return redirect("core:home")

        return render(request, "accounts/register.html", {"form": form})


class ActivateView(View):
    """تفعيل الحساب عن طريق اللينك"""
    def get(self, request, token):
        user_id = validate_activation_token(token)
        if not user_id:
            return render(
                request, "accounts/activation_result.html", {"status": "invalid"}
            )

        user = get_object_or_404(User, pk=user_id)
        if user.is_active:
            return render(
                request,
                "accounts/activation_result.html",
                {"status": "already_active"},
            )

        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. You can now log in.")
        return render(request, "accounts/activation_result.html", {"status": "ok"})


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = EmailAuthenticationForm


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "registration/password_reset_form.html"


