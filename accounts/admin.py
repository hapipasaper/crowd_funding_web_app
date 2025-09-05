from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


# Inline Profile (يظهر جوه صفحة اليوزر)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0  # ما يزودش فورمات فاضية
    fk_name = 'user'


# تخصيص عرض User في الـ Admin
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name', 'phone', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name',
                'phone', 'image', 'password1', 'password2',
                'is_active', 'is_staff'
            )}
        ),
    )

    inlines = [ProfileInline]  # ✅ نضيف Profile Inline هنا


# تسجيل الموديلات في Admin
admin.site.register(User, UserAdmin)