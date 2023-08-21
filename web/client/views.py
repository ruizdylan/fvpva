from web.base_view import BaseView


class CountriesView(BaseView):
    """
    Country manager base class.
    """

    # def check_permissions(self):
    #     if self.action in ('',):
    #         self.require_authentication()

    def dashboard(self):
        """
        Loads the country form.
        """
        return self.render('lookups/admin.html')
