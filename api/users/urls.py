from django.urls import path

from api.users.views import UserProfileUpdateView, UserProfilePasswordView, LoginView, \
    UpdatePassword, ForgotPasswordView, LogoutView, UserView, RegisterView, SocialLoginView

urlpatterns = [
    path("", UserView.as_view()),
    path("<int:pk>", UserView.as_view()),
    path("update-profile", UserProfileUpdateView.as_view(), ),
    path("update-password", UserProfilePasswordView.as_view()),
    path("login", LoginView.as_view(), name="client_login"),
    path("register", RegisterView.as_view(), name="client_register"),

    path('social-login', SocialLoginView.as_view()),

    # path("validate-otp", VerifyInvitationLink.as_view()),
    path("reset-password", UpdatePassword.as_view(), ),

    path("forgot-password", ForgotPasswordView.as_view(), ),

    path("logout", LogoutView.as_view()),

]
