from django.db import models
from django.utils import timezone

class Venta(models.Model):
    ESTADOS = [
        (1, 'Pagado'),
        (2, 'Devolucion Parcial'),
        (3, 'Devolucion Total')
    ]
    id_venta = models.AutoField(primary_key=True)
    correlativo_venta = models.CharField(max_length=20, unique=True, blank=True)
    fecha_venta = models.DateTimeField()
    id_usuario_venta = models.IntegerField()
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    estado_venta = models.IntegerField(choices=ESTADOS, default=1)

    def __str__(self):
        return f"Venta {self.correlativo_venta} - Total: {self.total_venta}"

    def save(self, *args, **kwargs):
        """Sobrescribimos save para generar el correlativo automáticamente"""
        if not self.correlativo_venta:  # Solo si no tiene correlativo
            self.correlativo_venta = self.generar_correlativo()
        super().save(*args, **kwargs)
    
    @classmethod
    def generar_correlativo(cls):
        """Genera un correlativo único con formato VENT-AÑONÚMERO
        Ejemplo: VENT-202600001, VENT-202600002, VENT-202700001, etc.
        """
        from django.db import transaction
        
        anio_actual = timezone.now().year
        
        # Usamos select_for_update dentro de una transacción para evitar concurrencia
        with transaction.atomic():
            # Buscar la última venta del año actual
            ultima_venta = cls.objects.select_for_update().filter(
                correlativo_venta__startswith=f"VENT-{anio_actual}"
            ).order_by('-id_venta').first()
            
            if ultima_venta:
                # Extraer el número: "VENT-202600123" -> 123
                try:
                    # Obtenemos todo el correlativo y extraemos solo la parte numérica después del año
                    correlativo_completo = ultima_venta.correlativo_venta
                    # VENT-202600123 -> extraemos "202600123" y luego tomamos los últimos 6 dígitos
                    numero_str = correlativo_completo.replace(f"VENT-{anio_actual}", "")
                    ultimo_numero = int(numero_str)
                    nuevo_numero = ultimo_numero + 1
                except (IndexError, ValueError):
                    nuevo_numero = 1
            else:
                # Primera venta del año: comienza en 1
                nuevo_numero = 1
            
            # Formato: 6 dígitos (máximo 999,999 ventas por año)
            # VENT-2026 + 000001 = VENT-2026000001
            return f"VENT-{anio_actual}{nuevo_numero:06d}"


class VentaPago(models.Model):
    PAGOS =[
        (1, 'Efectivo'),
        (2, 'Yape'),
        (3, 'Tarjeta'),
        (4, 'Transferencia'),
    ]
    id_pago = models.AutoField(primary_key=True)
    id_venta = models.IntegerField()
    forma_pago = models.IntegerField(choices=PAGOS)
    monto_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    efectivo_recibido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    efectivo_vuelto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.id_pago} - Venta {self.id_venta} - Forma: {self.get_forma_pago_display()}"


class DetalleVenta(models.Model):
    ESTADOS = [
        (1, 'Pagado'),
        (2, 'Devolucion Parcial'),
        (3, 'Devolucion Total')
    ]
    
    id_detalle = models.AutoField(primary_key=True)
    id_venta = models.IntegerField()
    descripcion_producto = models.CharField(max_length=255)
    codigo_barra = models.CharField(max_length=100)
    codigo_interno = models.CharField(max_length=20, blank=True)
    cantidad_venta = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    estado_venta = models.IntegerField(choices=ESTADOS, default=1)
    devolucion_cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    devolucion_monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    devolucion_fecha = models.DateTimeField(null=True, blank=True)
    usuario_actualizacion = models.IntegerField(null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return f"Detalle {self.id_detalle} - Venta {self.id_venta} - Producto: {self.descripcion_producto}"