from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from .models import Venta, VentaPago, DetalleVenta
from .serializers import VentaSerializer, VentaCreateSerializer

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