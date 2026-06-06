# serializers.py
from rest_framework import serializers
from .models import Kardex, TipoMovimiento

class TipoMovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMovimiento
        fields = ['id', 'codigo', 'nombre', 'tipo', 'activo']

class KardexSerializer(serializers.ModelSerializer):
    origen_movimiento = TipoMovimientoSerializer(read_only=True)
    
    class Meta:
        model = Kardex
        fields = [
            'id', 'codigo_interno', 'codigo_barra', 'nombre_producto',
            'origen_movimiento', 'cantidad', 'stock_anterior', 'stock_nuevo',
            'precio_compra', 'precio_venta', 'subtotal', 'correlativo_referencia',
            'id_venta', 'detalle_venta_id', 'fecha_movimiento', 'usuario_id'
        ]