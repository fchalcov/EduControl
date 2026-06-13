from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Kardex, TipoMovimiento
from .serializers import KardexSerializer, TipoMovimientoSerializer

# Configuración de paginación
class KardexPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# ============================================
# LISTAR TIPOS DE MOVIMIENTO
# ============================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tipo_movimiento_list(request):
    """
    Lista todos los tipos de movimiento activos
    """
    tipos = TipoMovimiento.objects.filter(activo=True).order_by('tipo', 'nombre')
    serializer = TipoMovimientoSerializer(tipos, many=True)
    return Response(serializer.data)

# ============================================
# LISTAR MOVIMIENTOS DE KARDEX CON FILTROS
# ============================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kardex_list(request):

    movimientos = Kardex.objects.all().order_by('fecha_movimiento')
    
    # Filtro por tipo de movimiento (Ingreso/Salida)
    tipo_movimiento = request.GET.get('tipo_movimiento', '')
    if tipo_movimiento:
        if tipo_movimiento in ['1', '2']:
            movimientos = movimientos.filter(origen_movimiento__tipo=int(tipo_movimiento))
    
    # Filtro por origen (código del tipo de movimiento)
    origen = request.GET.get('origen', '')
    if origen:
        movimientos = movimientos.filter(origen_movimiento__codigo=origen)
    
    # Filtro por búsqueda (producto, código interno, código de barras)
    search = request.GET.get('search', '')
    if search:
        movimientos = movimientos.filter(
            Q(nombre_producto__icontains=search) |
            Q(codigo_interno__icontains=search) |
            Q(codigo_barra__icontains=search)
        )
    
    # Filtro por rango de fechas
    fecha_desde = request.GET.get('fecha_desde', '')
    if fecha_desde:
        movimientos = movimientos.filter(fecha_movimiento__date__gte=fecha_desde)
    
    fecha_hasta = request.GET.get('fecha_hasta', '')
    if fecha_hasta:
        movimientos = movimientos.filter(fecha_movimiento__date__lte=fecha_hasta)
    
    # Paginación
    paginator = KardexPagination()
    paginated_movimientos = paginator.paginate_queryset(movimientos, request)
    serializer = KardexSerializer(paginated_movimientos, many=True)
    
    return paginator.get_paginated_response(serializer.data)