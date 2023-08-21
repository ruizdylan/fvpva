from django.urls import path

from api.order.views import OrderAPIView, OrderDataTableAPIView
from api.users.views import UserProfileUpdateView, UserProfilePasswordView, LoginView, \
    UpdatePassword, ForgotPasswordView, LogoutView, UserView, RegisterView, SocialLoginView

urlpatterns = [

    path("", OrderAPIView.as_view(), name="client-order"),
    path("<int:pk>", OrderAPIView.as_view(), name="client-order"),

    path("datatable", OrderDataTableAPIView.as_view(), name="order-datatable"),
]
