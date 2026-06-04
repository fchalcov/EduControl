from rest_framework import serializers
from .models import Venta, VentaPago, DetalleVenta

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = [
            'id_detalle', 'id_venta', 'descripcion_producto', 
            'codigo_barra', 'cantidad_venta', 'precio_venta', 
            'sub_total_venta', 'estado_venta'
        ]

class VentaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaPago
        fields = [
            'id_pago', 'id_venta', 'forma_pago', 
            'monto_pagar', 'efectivo_recibido', 'efectivo_vuelto'
        ]

class VentaSerializer(serializers.ModelSerializer):
    pagos = VentaPagoSerializer(many=True, read_only=True)
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venta
        fields = [
            'id_venta', 'correlativo_venta', 'fecha_venta',
            'id_usuario_venta', 'total_venta', 'estado_venta',
            'pagos', 'detalles'
        ]

class VentaCreateSerializer(serializers.Serializer):
    """Serializer para crear una venta completa"""
    id_usuario_venta = serializers.IntegerField()
    detalles = serializers.ListField(child=serializers.DictField())
    pagos = serializers.ListField(child=serializers.DictField())