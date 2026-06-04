from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Producto
from .serializers import ProductoSerializer

# Configuración de paginación
class ProductoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# ============================================
# 1. LISTAR PRODUCTOS
# ============================================
@api_view(['GET'])
def producto_list(request):
    productos = Producto.objects.all().order_by('-id')
    
    # Filtro por búsqueda
    search = request.GET.get('search', '')
    if search:
        productos = productos.filter(
            Q(nombre_producto__icontains=search) |
            Q(codigo_barra__icontains=search)
        )
    
    # Filtro por estado
    estado = request.GET.get('estado')
    if estado is not None:
        if estado.lower() == 'true':
            productos = productos.filter(estado=True)
        elif estado.lower() == 'false':
            productos = productos.filter(estado=False)
    
    # Paginación
    paginator = ProductoPagination()
    paginated_productos = paginator.paginate_queryset(productos, request)
    serializer = ProductoSerializer(paginated_productos, many=True, context={'request': request})
    
    return paginator.get_paginated_response(serializer.data)

# ============================================
# 2. OBTENER PRODUCTO POR ID
# ============================================
@api_view(['GET'])
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    serializer = ProductoSerializer(producto, context={'request': request})
    return Response(serializer.data)

# ============================================
# 3. CREAR PRODUCTO
# ============================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def producto_create(request):

    serializer = ProductoSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        producto = serializer.save()
        return Response(
            {
                'message': 'Producto creado exitosamente',
                'producto': ProductoSerializer(producto).data
            },
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        {
            'error': 'Error al crear el producto',
            'detalles': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

# ============================================
# 4. ACTUALIZAR PRODUCTO (TODOS LOS CAMPOS)
# ============================================
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    partial = request.method == 'PATCH'
    
    serializer = ProductoSerializer(
        producto, 
        data=request.data, 
        partial=partial, 
        context={'request': request}
    )
    
    if serializer.is_valid():
        producto_actualizado = serializer.save()
        return Response(
            {
                'message': 'Producto actualizado exitosamente',
                'producto': ProductoSerializer(producto_actualizado).data
            }
        )
    return Response(
        {
            'error': 'Error al actualizar el producto',
            'detalles': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

# ============================================
# 5. ELIMINAR PRODUCTO
# ============================================
@api_view(['DELETE'])
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    nombre_producto = producto.nombre_producto
    producto.delete()
    
    return Response(
        {
            'message': f'Producto "{nombre_producto}" eliminado exitosamente'
        },
        status=status.HTTP_200_OK
    )