from django.db import models
from django.utils import timezone
import random

class Producto(models.Model):

    codigo_interno = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    nombre_producto = models.CharField(max_length=250)
    cantidad_producto = models.IntegerField(default=0)
    costo_producto = models.DecimalField(max_digits=12, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    codigo_barra = models.CharField(max_length=100, blank=True)
    estado = models.BooleanField(default=True)
    
    usuario_creacion = models.IntegerField(null=True, blank=True)
    usuario_actualizacion = models.IntegerField(null=True, blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def generar_codigo_interno(self):
        ahora = timezone.now()
        
        año = ahora.strftime('%y')
        mes = ahora.strftime('%m')
        dia = ahora.strftime('%d')
        hora = ahora.strftime('%H')
        minuto = ahora.strftime('%M')
        segundo = ahora.strftime('%S')
        
        parte_fija = f"{año}{mes}{dia}{hora}{minuto}{segundo}"
        parte_aleatoria = str(random.randint(0, 9999)).zfill(4)
        
        return f"{parte_fija}{parte_aleatoria}"
    
    # ============================================
    # MÉTODOS PARA MANEJAR STOCK
    # ============================================
    def restar_stock(self, cantidad):
        """Resta stock de este producto"""
        if self.cantidad_producto >= cantidad:
            self.cantidad_producto -= cantidad
            self.save()
            return True
        return False
    
    def aumentar_stock(self, cantidad):
        """Aumenta stock de este producto"""
        self.cantidad_producto += cantidad
        self.save()
        return True
    
    def tiene_stock(self, cantidad):
        """Verifica si tiene suficiente stock"""
        return self.cantidad_producto >= cantidad
    
    def save(self, *args, **kwargs):
        if not self.codigo_interno:
            codigo = self.generar_codigo_interno()
            while Producto.objects.filter(codigo_interno=codigo).exists():
                codigo = self.generar_codigo_interno()
            self.codigo_interno = codigo
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.codigo_interno} - {self.nombre_producto}"