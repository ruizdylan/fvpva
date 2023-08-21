from django.urls import path, include

from .views.home import HomeView, PaymentMethodView

# from api.propertycontent.views import PropertyContentView

urlpatterns = [
    # Visitor Website
    path("", view=HomeView.as_view('index'), name="visitor-home"),
    path("free-numbers", view=HomeView.as_view('free_numbers'), name="visitor-free-numbers"),
    path("login", view=HomeView.as_view('login'), name="visitor-login"),
    path("sign-up", view=HomeView.as_view('signup'), name="visitor-signup"),
    path("payment-method", view=PaymentMethodView.as_view('index'), name="visitor-payment-method"),
    path("thank-you/<int:pk>", view=PaymentMethodView.as_view('thank_you'), name="visitor-thank-you"),
    # Admin Site
    path("administrator/", include("web.administrator.urls")),
    # Client Dashboard
    path("client/", include("web.client.urls")),
    path('set-auth-cookie/', HomeView.as_view('auth_cookie'), name="set-auth-cookie"),
    path('set-auth-cookie/<str:access_tokenFsirm>', HomeView.as_view('auth_cookie'), name="set-auth-cookie"),

]
