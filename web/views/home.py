import json

import requests
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import redirect

from api.order.models import UserWallet, Order
from api.services.models import Services
from fapva.utils import paypal_generate_access_token, paypal_generate_client_access_token
from main.models import Countries
from web.base_view import BaseView
from web.decorators import logout_required
from paypal.standard.forms import PayPalPaymentsForm


class HomeView(BaseView):

    def index(self, *args, **kwargs):
        return self.render('visitor/home.html')

    def free_numbers(self):
        return self.render("visitor/free_numbers.html")

    def login(self):
        self.next = self.request.GET.get('next', "")
        if self.request.user.is_authenticated:
            return redirect("/")
        return self.render("visitor/login.html")

    def signup(self):
        self.next = self.request.GET.get('next', "")
        if self.request.user.is_authenticated:
            return redirect("/")
        return self.render("visitor/signup.html")

    def auth_cookie(self, *args, **kwargs):
        """
        Intermediate view to set authorization cookie.
        :param args: list arguments
        :param kwargs: dict arguments with keys
        :return: HTTP redirect response.
        """
        access_token = kwargs.get('access_token', '')
        response = self.redirect('home')
        response.set_cookie('u-at', access_token)
        return response


class PaymentMethodView(BaseView):

    def index(self, *args, **kwargs):
        number_id = self.request.GET.get('number_id', 0)
        if not self.request.user.is_authenticated:
            return redirect(f"/login?next=/payment-method?number_id={number_id}")
        if number_id:
            self.access_token = paypal_generate_access_token()
            self.client_token = paypal_generate_client_access_token(self.access_token)
            self.client_id = settings.PAYPAL_CLIENT_ID
        self.number_id = number_id
        return self.render('visitor/payment-method.html')

    def thank_you(self, *args, **kwargs):
        try:
            if not self.request.user.is_authenticated:
                return redirect(f"/login")
            pk = kwargs.get("pk")
            order_instance = Order.objects.get(id=pk)
            self.expire_at = order_instance.expire_at
            return self.render('visitor/thank-you.html')
        except Order.DoesNotExist:
            return self.render("RecordDoesNotExists.html")


    def auth_cookie(self, *args, **kwargs):
        """
        Intermediate view to set authorization cookie.
        :param args: list arguments
        :param kwargs: dict arguments with keys
        :return: HTTP redirect response.
        """
        access_token = kwargs.get('access_token', '')
        response = self.redirect('home')
        response.set_cookie('u-at', access_token)
        return response
