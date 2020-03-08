from django.urls import path, include

from .views import (
    LoginAPIView,
    RegistrationAPIView,
    UserRetrieveUpdateAPIView,
    ActivateUserAccount,
    PasswordResetView,
    GoogleView,
    FacebookView,
)


urlpatterns = [
    path("user/", UserRetrieveUpdateAPIView.as_view()),
    path("users/", RegistrationAPIView.as_view()),
    path("users/login/", LoginAPIView.as_view()),
    path('auth/google/', GoogleView.as_view()),
    path('auth/facebook/', FacebookView.as_view()),
    path("users/activate/<uidb64>/<token>/", ActivateUserAccount.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls'),
    path("reset-password/<token>", PasswordResetView.as_view()),
]
