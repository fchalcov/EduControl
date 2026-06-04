from django.db import models

class Producto(models.Model):

    nombre_producto = models.CharField(max_length=250)
    cantidad_producto = models.IntegerField(default=0)
    costo_producto = models.DecimalField(max_digits=12, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    codigo_barra = models.CharField(max_length=100, blank=True)
    estado = models.BooleanField(default=True)
    
    # Relaciones
    usuario_creacion = models.IntegerField(null=True, blank=True)
    usuario_actualizacion = models.IntegerField(null=True, blank=True)
    
    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre_producto