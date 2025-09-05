from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
from .validators import egypt_phone_validator
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    # نستخدم الإيميل لتسجيل الدخول
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, validators=[egypt_phone_validator])
    image = models.ImageField(
        upload_to='profiles/',
        blank=True, null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # مطلوبة لإنشاء سوبر يوزر

    def _str_(self):
        return self.email or self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birthdate = models.DateField(blank=True, null=True)
    facebook_profile = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def _str_(self):
        return f"Profile({self.user})"


# ------- Signals -------
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()