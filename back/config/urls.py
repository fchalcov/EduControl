from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView


class PublicTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("apps.usuario.urls")),
    path("menu/", include("apps.menu.urls")),
    path("rol/", include("apps.rol.urls")),
    path("producto/", include("apps.producto.urls")),
    path("venta/", include("apps.venta.urls")),
    path(
        "api/token/refresh/",
        PublicTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
