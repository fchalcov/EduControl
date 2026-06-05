# apps/venta/signals.py
from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from .models import DetalleVenta, Venta
from apps.kardex.models import Kardex, TipoMovimiento
from apps.producto.models import Producto

@receiver(post_save, sender=DetalleVenta)
def registrar_kardex_al_vender(sender, instance, created, **kwargs):
    """
    Cuando se crea un DetalleVenta, registra en Kardex
    Si falla, cancela toda la transacción
    """
    if not created:
        return
    
    print("Registrando en Kardex...")
    
    # Obtener el producto por su código interno
    producto = Producto.objects.get(codigo_interno=instance.codigo_interno)
    
    # Obtener el tipo de movimiento VENTA
    tipo_venta = TipoMovimiento.objects.get(codigo='VENTA')
    
    # Obtener la venta
    venta = Venta.objects.get(id_venta=instance.id_venta)
    
    # Calcular stock anterior
    ultimo_kardex = Kardex.objects.filter(
        codigo_interno=producto.codigo_interno
    ).order_by('-fecha_movimiento').first()
    
    if ultimo_kardex:
        stock_anterior = ultimo_kardex.stock_nuevo
    else:
        stock_anterior = producto.cantidad_producto + int(instance.cantidad_venta)
    
    # Crear registro en Kardex (si falla, la transacción se cancela)
    Kardex.objects.create(
        codigo_interno=producto.codigo_interno,
        codigo_barra=producto.codigo_barra,
        nombre_producto=producto.nombre_producto,
        origen_movimiento=tipo_venta,
        cantidad=int(instance.cantidad_venta),
        stock_anterior=stock_anterior,
        stock_nuevo=producto.cantidad_producto,
        precio_costo=0, ## SOLO PARA INGRESO NUEVOS
        precio_venta=float(instance.precio_venta),
        subtotal=float(instance.sub_total_venta),
        correlativo_referencia=venta.correlativo_venta,
        id_venta=instance.id_venta,
        detalle_venta_id=instance.id_detalle,
        usuario_id=venta.id_usuario_venta
    )
    
    print(f"Kardex registrado: {producto.nombre_producto}")