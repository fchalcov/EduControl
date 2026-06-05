from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Prefetch
from django.db import transaction
from .serializers import MenuListSerializer, MenuSaveSerializer
from apps.menu.models import Menu
from apps.rol.models import RolMenu
from apps.usuario.models import UsuarioRol, UsuarioMenu

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_menu_x_usuario(request):

    user = request.user

    try:
        usuario_rol = UsuarioRol.objects.get(usuario=user)
    except UsuarioRol.DoesNotExist:
        return Response([])

    rol = usuario_rol.usuario_rol

    role_menu_ids = RolMenu.objects.filter(
        rol=rol
    ).values_list('menu_id', flat=True)

    user_menu_ids = UsuarioMenu.objects.filter(
        usuario=user,
        permiso_ver=True
    ).values_list('menu_id', flat=True)

    menu_ids = set(role_menu_ids) | set(user_menu_ids)

    menus = Menu.objects.filter(
        id__in=menu_ids,
        menu_padre__isnull=True,
        menu_activo=True
    ).prefetch_related(
        Prefetch(
            'menus_hijos',
            queryset=Menu.objects.filter(
                id__in=menu_ids,
                menu_activo=True
            ).order_by('menu_orden'),
            to_attr='children_list'
        )
    ).order_by('menu_orden')
    serializer = MenuListSerializer(menus, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_menu(request):

    menus = Menu.objects.filter(
        menu_padre__isnull=True,
    ).prefetch_related(
        Prefetch(
            'menus_hijos',
            queryset=Menu.objects.filter(menu_activo=True).order_by('menu_orden'),
            to_attr='children_list'
        )
    ).order_by('menu_orden')

    serializer = MenuListSerializer(menus, many=True)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_menu(request):
    data = request.data

    serializer = MenuSaveSerializer(data=data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    validated_data = serializer.validated_data

    try:
        with transaction.atomic():
            menu_id = validated_data.get('id')

            if menu_id:
                # ACTUALIZAR
                menu = Menu.objects.get(id=menu_id)
                menu.menu_titulo = validated_data.get('menu_titulo')
                menu.menu_ruta = validated_data.get('menu_ruta')
                menu.menu_icono = validated_data.get('menu_icono')
                menu.menu_orden = validated_data.get('menu_orden')
                menu.menu_activo = validated_data.get('menu_activo')
                padre_id = validated_data.get('menu_padre_id')
                menu.menu_padre_id = padre_id if padre_id else None
                menu.save()
            else:
                # CREAR
                menu = Menu.objects.create(**validated_data)
                
        return Response({
            "message": "Menu guardado correctamente",
            "menu_id": menu.id
        })
    except Menu.DoesNotExist:
        return Response({"error": "Menu no encontrado"}, status=404)

    except Exception:
        return Response({"error": "Error al guardar el menú"}, status=400)

