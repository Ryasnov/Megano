from django.urls import path

from .views import (
    SignInView,
    SignUpView,
    signOut,
    ProfileView,
    ChangePasswordView,
    ChangeAvatarView,
)

urlpatterns = [
    path("sign-in/", SignInView.as_view()),
    path("sign-up/", SignUpView.as_view()),
    path("sign-out/", signOut),
    path("profile/", ProfileView.as_view()),
    path("profile/password/", ChangePasswordView.as_view()),
    path("profile/avatar/", ChangeAvatarView.as_view()),
]
