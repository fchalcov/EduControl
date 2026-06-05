from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from .models import Venta, VentaPago, DetalleVenta
from .serializers import VentaSerializer, VentaCreateSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Sum

# ============================================
# PAGINACIÓN PARA VENTAS
# ============================================
class VentaPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['POST'])
@transaction.atomic
def crear_venta(request):
    serializer = VentaCreateSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    # Generar correlativo automático
    ultima_venta = Venta.objects.order_by('-id_venta').first()
    nuevo_correlativo = f"V-{ultima_venta.id_venta + 1:06d}" if ultima_venta else "V-000001"
    
    # Crear la venta
    venta = Venta.objects.create(
        correlativo_venta=nuevo_correlativo,
        fecha_venta=timezone.now(),
        id_usuario_venta=data['id_usuario_venta'],
        total_venta=sum(d['sub_total_venta'] for d in data['detalles']),
        estado_venta=1
    )
    
    # Crear detalles
    for detalle_data in data['detalles']:
        DetalleVenta.objects.create(
            id_venta=venta.id_venta,
            descripcion_producto=detalle_data['descripcion_producto'],
            codigo_barra=detalle_data.get('codigo_barra', ''),
            cantidad_venta=detalle_data['cantidad_venta'],
            precio_venta=detalle_data['precio_venta'],
            sub_total_venta=detalle_data['sub_total_venta']
        )
    
    # Crear pagos
    for pago_data in data['pagos']:
        VentaPago.objects.create(
            id_venta=venta.id_venta,
            forma_pago=pago_data['forma_pago'],
            monto_pagar=pago_data['monto_pagar'],
            efectivo_recibido=pago_data.get('efectivo_recibido'),
            efectivo_vuelto=pago_data.get('efectivo_vuelto')
        )
    
    return Response({
        'success': True,
        'venta_id': venta.id_venta,
        'correlativo': venta.correlativo_venta,
        'message': 'Venta registrada exitosamente'
    }, status=status.HTTP_201_CREATED)

# ============================================
# 1. LISTAR VENTAS
# ============================================
@api_view(['GET'])
def venta_list(request):
    ventas = Venta.objects.all().order_by('-id_venta')
    
    # Filtro por número de venta
    search = request.GET.get('search', '')
    if search:
        ventas = ventas.filter(correlativo_venta__icontains=search)
    
    # Filtro por estado
    estado = request.GET.get('estado')
    if estado and estado.isdigit():
        ventas = ventas.filter(estado_venta=int(estado))
    
    # Filtro por fecha exacta
    fecha = request.GET.get('fecha')
    if fecha:
        ventas = ventas.filter(fecha_venta__date=fecha)
    
    # Filtro por mes
    mes = request.GET.get('mes')
    if mes:
        ventas = ventas.filter(fecha_venta__year=mes[:4], fecha_venta__month=mes[5:])
    
    # Filtro por rango de fechas
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    if fecha_desde and fecha_hasta:
        ventas = ventas.filter(fecha_venta__date__gte=fecha_desde, fecha_venta__date__lte=fecha_hasta)
    
    # Paginación
    paginator = VentaPagination()
    paginated_ventas = paginator.paginate_queryset(ventas, request)
    
    # Construir respuesta con datos adicionales
    result = []
    for venta in paginated_ventas:
        # Obtener pagos de la venta
        pagos = VentaPago.objects.filter(id_venta=venta.id_venta)
        
        # Calcular total devuelto
        detalles = DetalleVenta.objects.filter(id_venta=venta.id_venta)
        devolucion_total_monto = detalles.aggregate(total=Sum('devolucion_monto'))['total'] or 0
        
        venta_data = {
            'id_venta': venta.id_venta,
            'correlativo_venta': venta.correlativo_venta,
            'fecha_venta': venta.fecha_venta,
            'total_venta': float(venta.total_venta),
            'estado_venta': venta.estado_venta,
            'devolucion_total_monto': float(devolucion_total_monto),
            'pagos': [
                {
                    'id_pago': p.id_pago,
                    'forma_pago': p.forma_pago,
                    'monto_pagar': float(p.monto_pagar),
                    'efectivo_recibido': float(p.efectivo_recibido) if p.efectivo_recibido else None,
                    'efectivo_vuelto': float(p.efectivo_vuelto) if p.efectivo_vuelto else None
                } for p in pagos
            ]
        }
        result.append(venta_data)
    
    return paginator.get_paginated_response(result)

# ============================================
# 2. DETALLE DE VENTA
# ============================================
@api_view(['GET'])
def venta_detail(request, pk):
    try:
        venta = Venta.objects.get(pk=pk)
    except Venta.DoesNotExist:
        return Response({'error': 'Venta no encontrada'}, status=404)
    
    # Obtener pagos
    pagos = VentaPago.objects.filter(id_venta=venta.id_venta)
    
    # Obtener detalles de productos
    detalles = DetalleVenta.objects.filter(id_venta=venta.id_venta)
    
    # Calcular total devuelto
    devolucion_total_monto = detalles.aggregate(total=Sum('devolucion_monto'))['total'] or 0
    
    venta_data = {
        'id_venta': venta.id_venta,
        'correlativo_venta': venta.correlativo_venta,
        'fecha_venta': venta.fecha_venta,
        'total_venta': float(venta.total_venta),
        'estado_venta': venta.estado_venta,
        'devolucion_total_monto': float(devolucion_total_monto),
        'pagos': [
            {
                'id_pago': p.id_pago,
                'forma_pago': p.forma_pago,
                'monto_pagar': float(p.monto_pagar),
                'efectivo_recibido': float(p.efectivo_recibido) if p.efectivo_recibido else None,
                'efectivo_vuelto': float(p.efectivo_vuelto) if p.efectivo_vuelto else None
            } for p in pagos
        ],
        'detalles': [
            {
                'id_detalle': d.id_detalle,
                'descripcion_producto': d.descripcion_producto,
                'codigo_barra': d.codigo_barra,
                'cantidad_venta': float(d.cantidad_venta),
                'precio_venta': float(d.precio_venta),
                'sub_total_venta': float(d.sub_total_venta),
                'estado_venta': d.estado_venta,
                'devolucion_cantidad': float(d.devolucion_cantidad),
                'devolucion_monto': float(d.devolucion_monto)
            } for d in detalles
        ]
    }
    
    return Response(venta_data)