from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
from django.db.models import Prefetch

from apps.rol.models import Rol, RolMenu
from apps.menu.models import Menu
from apps.rol.serializers import RolListSerializer, RolSaveSerializer, MenuRolListSerializer


# LISTAR ROLES
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_rol(request):
    roles = Rol.objects.order_by('id')
    serializer = RolListSerializer(roles, many=True)
    return Response(serializer.data)


# CREAR / ACTUALIZAR ROL
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_rol(request):

    data = request.data
    rol_data = data.get('rol')
    menus = data.get('menus', [])

    serializer = RolSaveSerializer(data=rol_data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    validated_data = serializer.validated_data

    try:
        with transaction.atomic():

            rol_id = validated_data.get('id')

            if rol_id:
                # ACTUALIZAR
                rol = Rol.objects.get(id=rol_id)
                rol.rol_nombre = validated_data.get('rol_nombre')
                rol.rol_descripcion = validated_data.get('rol_descripcion')
                rol.rol_activo = validated_data.get('rol_activo')
                rol.save()
            else:
                # CREAR
                rol = Rol.objects.create(**validated_data)

            # MENUS ACTUALES
            current_menus = set(
                RolMenu.objects.filter(rol=rol)
                .values_list('menu_id', flat=True)
            )

            # MENUS NUEVOS
            new_menus = set(menus)

            # DIFERENCIAS
            to_add = new_menus - current_menus
            to_remove = current_menus - new_menus

            # INSERTAR NUEVOS
            RolMenu.objects.bulk_create([
                RolMenu(rol=rol, menu_id=menu_id)
                for menu_id in to_add
            ])

            # ELIMINAR LOS QUE YA NO ESTÁN
            RolMenu.objects.filter(
                rol=rol,
                menu_id__in=to_remove
            ).delete()

        return Response({
            "message": "Rol y permisos guardados correctamente",
            "rol_id": rol.id
        })

    except Rol.DoesNotExist:
        return Response({"error": "Rol no encontrado"}, status=404)

    except Exception:
        return Response({"error": "Error al guardar el rol"}, status=400)

# LISTAR MENÚ POR ROL (CON CHECKED)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_rol_x_menu(request, rol_id):

    role_menu_ids = set(
        RolMenu.objects.filter(rol_id=rol_id)
        .values_list('menu_id', flat=True)
    )

    menus = Menu.objects.filter(
        menu_padre__isnull=True,
        menu_activo=True
    ).prefetch_related(
        Prefetch(
            'menus_hijos',
            queryset=Menu.objects.filter(menu_activo=True).order_by('menu_orden'),
            to_attr='children_list'
        )
    ).order_by('menu_orden')

    serializer = MenuRolListSerializer(
        menus,
        many=True,
        context={'role_menu_ids': role_menu_ids}
    )

    return Response(serializer.data)