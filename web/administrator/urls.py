from django.urls import path

from web.administrator.views import DashboardAdminWebView

urlpatterns = [

    path('dashboard', DashboardAdminWebView.as_view('dashboard'), name='admin-dashboard'),
    path('countries', DashboardAdminWebView.as_view('countries'), name='admin-countries'),
    path('services', DashboardAdminWebView.as_view('services'), name='admin-services'),
    path('services-numbers', DashboardAdminWebView.as_view('services_numbers'), name='admin-services-numbers'),
    path('bought-services', DashboardAdminWebView.as_view('bought_services'), name='admin-bought-services'),

]
