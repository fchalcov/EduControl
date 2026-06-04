from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para auditoría
    fecha_creacion = serializers.DateTimeField(read_only=True)
    fecha_actualizacion = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre_producto',
            'cantidad_producto',
            'costo_producto',
            'precio_unitario',
            'codigo_barra',
            'estado',
            'usuario_creacion',
            'usuario_actualizacion',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'usuario_creacion', 'fecha_actualizacion']
    
    def validate_nombre_producto(self, value):
        """Validar que el nombre no exceda 250 caracteres"""
        if len(value) > 250:
            raise serializers.ValidationError("El nombre del producto no puede exceder 250 caracteres")
        return value
    
    def validate_cantidad_producto(self, value):
        """Validar que la cantidad no sea negativa"""
        if value < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa")
        return value
    
    def validate_costo_producto(self, value):
        """Validar que el costo no sea negativo"""
        if value < 0:
            raise serializers.ValidationError("El costo no puede ser negativo")
        return value
    
    def validate_precio_unitario(self, value):
        """Validar que el precio unitario no sea negativo"""
        if value < 0:
            raise serializers.ValidationError("El precio unitario no puede ser negativo")
        return value
    
    def create(self, validated_data):
        """Crear producto automáticamente con usuario de creación"""
        # Si hay usuario autenticado, asignarlo automáticamente
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['usuario_creacion'] = request.user.id
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Actualizar producto automáticamente con usuario de actualización"""
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['usuario_actualizacion'] = request.user.id
        
        return super().update(instance, validated_data)