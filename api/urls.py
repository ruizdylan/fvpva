import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework_simplejwt import views as jwt_views
import oauth2_provider.views as oauth2_views


urlpatterns = [

                  path("users/", include("api.users.urls")),
                  path("main/", include("api.main.urls")),
                  path("services/", include("api.services.urls")),
                  path("order/", include("api.order.urls")),
                  path('debug/', include(debug_toolbar.urls)),
                  path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

                  re_path(r'^oauth/authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
                  re_path(r'^oauth/token/$', oauth2_views.TokenView.as_view(), name="token"),
                  re_path(r'^oauth/revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
                  #
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
