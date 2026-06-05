from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    """Página principal de la API (Browsable API de Django REST Framework)."""
    return Response(
        {
            "admin": request.build_absolute_uri("/admin/"),
            "autenticacion": {
                "login": request.build_absolute_uri("/user/login_usuario/"),
                "refresh_token": request.build_absolute_uri("/api/token/refresh/"),
            },
            "usuarios": {
                "listar": request.build_absolute_uri("/user/list_usuario/"),
            },
            "menu": {
                "por_usuario": request.build_absolute_uri("/menu/list_menu_x_usuario/"),
                "listar": request.build_absolute_uri("/menu/list_menu/"),
                "guardar": request.build_absolute_uri("/menu/save_menu/"),
            },
            "roles": {
                "listar": request.build_absolute_uri("/rol/list_rol/"),
                "menu_por_rol": request.build_absolute_uri("/rol/list_rol_x_menu/1/"),
                "guardar": request.build_absolute_uri("/rol/save_rol/"),
            },
            "productos": {
                "listar": request.build_absolute_uri("/producto/producto_list/"),
                "detalle": request.build_absolute_uri("/producto/producto_detail/1/"),
                "crear": request.build_absolute_uri("/producto/producto_create/"),
                "actualizar": request.build_absolute_uri("/producto/producto_update/1/"),
                "eliminar": request.build_absolute_uri("/producto/producto_delete/1/"),
            },
            "ventas": {
                "crear": request.build_absolute_uri("/venta/venta_create/"),
            },
        }
    )


def home_redirect(request):
    return redirect("api-root")
