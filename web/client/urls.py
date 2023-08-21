from django.urls import path

from web.client.views import CountriesView

urlpatterns = [

    path('', CountriesView.as_view('dashboard'), name='client-dashboard'),

]
