from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import Avatar, Profile


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор модели Avatar"""

    src = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def get_src(self, obj) -> str:
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор модели Profile"""

    avatar = AvatarSerializer()

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]
