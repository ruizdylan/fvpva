from django.urls import path

from api.main.views import CountriesDataTableAPIView, CountriesStatusUpdateAPIView, CountriesAPIView, \
    CountriesDeleteAPIView, PaypalOrderAPIView, PaypalOrderCaptureAPIView, OrderCancelAPIView, OrderWalletPayAPIView
from api.users.views import UserProfileUpdateView, UserProfilePasswordView, LoginView, \
    UpdatePassword, ForgotPasswordView, LogoutView, UserView, RegisterView

urlpatterns = [

    path("countries", CountriesAPIView.as_view(), name="countries"),
    path("countries/<int:pk>", CountriesAPIView.as_view(), name="countries"),

    path("countries-delete", CountriesDeleteAPIView.as_view(), name="countries-delete"),
    path("countries-delete/<int:pk>", CountriesDeleteAPIView.as_view(), name="countries-delete"),

    path("countries-datatable", CountriesDataTableAPIView.as_view(), name="countries-datatable"),

    path("countries/status", CountriesStatusUpdateAPIView.as_view(), name="countries-status"),
    path("countries/status/<int:pk>", CountriesStatusUpdateAPIView.as_view(), name="countries-status"),

    path("paypal/order", PaypalOrderAPIView.as_view(), name="paypal-order"),
    path("paypal/orders/<str:pk>/capture", PaypalOrderCaptureAPIView.as_view(), name="paypal-order"),


    path("order/cancel", OrderCancelAPIView.as_view(), name="cancel-order"),
    path("order/cancel/<str:pk>", OrderCancelAPIView.as_view(), name="cancel-order"),


    path("order/wallet-pay", OrderWalletPayAPIView.as_view(), name="wallet-order"),
    path("order/wallet-pay/<str:pk>", OrderWalletPayAPIView.as_view(), name="wallet-order"),

]
