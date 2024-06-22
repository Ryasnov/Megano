import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Profile, Avatar
from .serializers import ProfileSerializer


def signOut(request):
    """View функция для выхода из системы"""

    logout(request)
    return Response(status=status.HTTP_200_OK)


class SignInView(APIView):
    """Class-Based View для входа в систему"""

    def post(self, request: Request) -> Response:
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        username = user_data.get("username")
        password = user_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    """Class-Based View для регистрации"""

    def post(self, request: Request) -> Response:
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")

        try:
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.create(user=user, fullName=name)
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileView(APIView):
    """Class-Based View для профиля"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        try:
            profile = Profile.objects.get(user=request.user.id)
            email = request.data["email"]
            phone = request.data["phone"]
            fullname = request.data["fullName"]
            profile.email = email
            profile.phone = phone
            profile.fullName = fullname
            profile.save()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """Class-Based View для смены пароля"""

    def post(self, request: Request) -> Response:
        user = request.user
        data = request.data
        current_password = data.pop("passwordCurrent")
        new_password = data.pop("password")
        try:
            validate_password(new_password)
        except Exception:
            raise ValidationError("New password is invalid")
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ValidationError("Incorrect password")


class ChangeAvatarView(APIView):
    """Class-Based View для смены аватара"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        avatar = request.FILES["avatar"]
        profile = Profile.objects.get(user=request.user)

        if "default.jpg" not in str(profile.avatar.src):
            profile.avatar.src.delete(save=False)
        profile.avatar.delete()

        if str(avatar).lower().endswith(("jpg", "png", "jpeg")):
            profile_avatar = Avatar.objects.create(src=avatar)
            profile.avatar = profile_avatar
            profile.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
