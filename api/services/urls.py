from django.urls import path

from api.services.views import ServicesDataTableAPIView, ServicesStatusUpdateAPIView, ServicesAPIView, \
    ServicesDeleteAPIView, ServicesCountryNumberAPIView, ServicesNumberDataTableAPIView, \
    ServicesNumberStatusUpdateAPIView, ServicesNumberDeleteAPIView
from api.users.views import UserProfileUpdateView, UserProfilePasswordView, LoginView, \
    UpdatePassword, ForgotPasswordView, LogoutView, UserView, RegisterView

urlpatterns = [
    # Services
    path("", ServicesAPIView.as_view(), name="services"),
    path("<int:pk>", ServicesAPIView.as_view(), name="services"),

    path("delete", ServicesDeleteAPIView.as_view(), name="services-delete"),
    path("delete/<int:pk>", ServicesDeleteAPIView.as_view(), name="services-delete"),

    path("datatable", ServicesDataTableAPIView.as_view(), name="services-datatable"),

    path("status", ServicesStatusUpdateAPIView.as_view(), name="services-status"),
    path("status/<int:pk>", ServicesStatusUpdateAPIView.as_view(), name="services-status"),

    # Services Number
    path("country/number", ServicesCountryNumberAPIView.as_view(), name="services-country-number"),
    path("country/number/<int:pk>", ServicesCountryNumberAPIView.as_view(), name="services-country-number"),

    path("country/number/delete", ServicesNumberDeleteAPIView.as_view(), name="services-country-number-delete"),
    path("country/number/delete/<int:pk>", ServicesNumberDeleteAPIView.as_view(), name="services-country-number-delete"),

    path("country/number/status", ServicesNumberStatusUpdateAPIView.as_view(), name="services-country-number-status"),
    path("country/number/status/<int:pk>", ServicesNumberStatusUpdateAPIView.as_view(),
         name="services-country-number-status"),

    path("country/number/datatable", ServicesNumberDataTableAPIView.as_view(), name="services-country-number-datatable"),

]
