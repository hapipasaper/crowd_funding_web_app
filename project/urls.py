from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

    # روابط الحسابات
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path("accounts/", include("allauth.urls")),
       path("", include("core.urls", namespace="core")), 
    # 🔹 Password Reset URLs
    # صفحة إدخال الإيميل
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),
        name="password_reset",
    ),
    path("projects/", include("projects.urls", namespace="projects")),  # هنا ربطنا projects app
    path('logout/', auth_views.LogoutView.as_view(), name='logout_global'),


    # صفحة تأكيد إن الإيميل اتبعت
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
        name="password_reset_done",
    ),

    # صفحة تغيير الباسورد من اللينك
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),

    # صفحة نجاح تغيير الباسورد
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
        name="password_reset_complete",)
     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)