from django.db import models

class TipoMovimiento(models.Model):
    """
    Catálogo de orígenes de movimientos de inventario
    """
    TIPO_CHOICES = [
        (1, 'Ingreso'),
        (2, 'Salida'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    tipo = models.IntegerField(choices=TIPO_CHOICES)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Tipo de Movimiento'
        verbose_name_plural = 'Tipos de Movimientos'
        ordering = ['tipo', 'nombre']


class Kardex(models.Model):
    
    # ========================================
    # DATOS DEL PRODUCTO EN EL MOMENTO DEL MOVIMIENTO
    # ========================================
    codigo_interno = models.CharField(max_length=20)  # Código único del producto
    codigo_barra = models.CharField(max_length=100, blank=True)  # Código de barras
    nombre_producto = models.CharField(max_length=250)  # Nombre en ese momento
    
    # RELACIÓN CON TIPO DE MOVIMIENTO
    origen_movimiento = models.ForeignKey(TipoMovimiento, on_delete=models.PROTECT, related_name='movimientos')
    
    # CANTIDADES
    cantidad = models.IntegerField()
    stock_anterior = models.IntegerField()
    stock_nuevo = models.IntegerField()
    
    # PRECIOS
    # - Para Ingreso (Compra): precio_costo = precio de compra
    # - Para Salida (Venta): precio_venta = precio de venta, precio_costo = costo del producto
    precio_costo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # REFERENCIA
    correlativo_referencia = models.CharField(max_length=50, blank=True)
    
    # PARA VENTAS ESPECÍFICAMENTE
    id_venta = models.IntegerField(null=True, blank=True)
    detalle_venta_id = models.IntegerField(null=True, blank=True)
    
    # AUDITORÍA
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    usuario_id = models.IntegerField()
    
    def __str__(self):
        tipo_texto = "Ingreso" if self.origen_movimiento.tipo == 1 else "Salida"
        return f"{tipo_texto} - {self.origen_movimiento.nombre} - {self.nombre_producto} - {self.cantidad}"
    
    class Meta:
        ordering = ['-fecha_movimiento']