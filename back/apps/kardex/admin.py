from django.contrib import admin
from .models import Kardex, TipoMovimiento

# admin.site.register(Kardex)
# admin.site.register(TipoMovimiento)

@admin.register(TipoMovimiento)
class TipoMovimientoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'activo']
    list_filter = ['tipo', 'activo']
    search_fields = ['codigo', 'nombre']

@admin.register(Kardex)
class KardexAdmin(admin.ModelAdmin):
    list_display = ['fecha_movimiento', 'nombre_producto', 'origen_movimiento', 'cantidad', 'stock_nuevo']
    list_filter = ['origen_movimiento', 'fecha_movimiento']
    search_fields = ['nombre_producto', 'codigo_interno', 'correlativo_referencia']
    readonly_fields = ['fecha_movimiento']