from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView

from .views import api_root, home_redirect


class PublicTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


urlpatterns = [
    path("", home_redirect),
    path("api/", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("user/", include("apps.usuario.urls")),
    path("menu/", include("apps.menu.urls")),
    path("rol/", include("apps.rol.urls")),
    path("producto/", include("apps.producto.urls")),
    path("venta/", include("apps.venta.urls")),
    path("kardex/", include("apps.kardex.urls")),
    path(
        "api/token/refresh/",
        PublicTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
