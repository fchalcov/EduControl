from django.contrib import admin
from .models import Venta, DetalleVenta, VentaPago
# Register your models here.

admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(VentaPago)