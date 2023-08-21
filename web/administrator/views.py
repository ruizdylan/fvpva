import json

from api.order.models import Order
from api.services.models import Services, ServiceNumber
from main.models import Countries
from web.base_view import BaseView


class DashboardAdminWebView(BaseView):
    """
    Country manager base class.
    """

    def check_permissions(self):
        # if self.action in ('dashboard', 'countries', "services", "services_numbers"):
        self.is_super_admin_authenticated()

    def dashboard(self):
        """
        Loads the country form.
        """
        self.countries = Countries.objects.filter(is_active=True, is_deleted=False).count()
        self.services = Services.objects.filter(is_active=True, is_deleted=False).count()
        self.numbers = ServiceNumber.objects.filter(is_active=True, is_deleted=False).count()
        self.orders = Order.objects.filter(is_completed=True).count()
        return self.render('administrator/dashboard.html')

    def countries(self):
        return self.render('administrator/countries.html')

    def services(self):
        return self.render('administrator/services.html')

    def services_numbers(self):
        self.services = json.dumps(list(Services.objects.filter(is_active=True, is_deleted=False).values("id", "name")))
        self.countries = json.dumps(list(Countries.objects.filter(is_active=True, is_deleted=False).values("id", "name")))
        return self.render('administrator/services-numbers.html')

    def bought_services(self):
        self.services = json.dumps(list(Services.objects.filter(is_active=True, is_deleted=False).values("id", "name")))
        self.countries = json.dumps(list(Countries.objects.filter(is_active=True, is_deleted=False).values("id", "name")))
        return self.render('administrator/bought-services-numbers.html')
