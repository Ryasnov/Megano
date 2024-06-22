from django.db import models
from django.contrib.auth.models import User


class Avatar(models.Model):
    """Модель аватара пользователя"""

    src = models.ImageField(
        upload_to="app_profiles/",
        default="app_profiles/default.jpg",
        verbose_name="Link",
    )
    alt = models.CharField(max_length=128, verbose_name="Description")
    objects = models.Manager()

    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatars"

    @classmethod
    def get_default(cls):
        avatar, _ = cls.objects.get_or_create(src="app_profiles/default.jpg")
        return avatar.pk


class Profile(models.Model):
    """Модель профиля пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(max_length=128, verbose_name="full name")
    phone = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="phone number"
    )
    balance = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name="balance"
    )
    avatar = models.ForeignKey(
        Avatar,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Avatar",
        default=Avatar.get_default,
    )
    email = models.EmailField(blank=True, null=True, unique=True, verbose_name="email")
    objects = models.Manager()

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        return f"login - {self.user.username}; name - {self.fullName}"
