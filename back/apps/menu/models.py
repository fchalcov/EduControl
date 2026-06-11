from django.db import models


class Menu(models.Model):

    menu_titulo = models.CharField(max_length=100)
    menu_ruta   = models.CharField(max_length=200, blank=True, null=True)
    menu_icono  = models.CharField(max_length=50, blank=True, default='ListBulletIcon')
    menu_padre  = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='menus_hijos'
    )
    menu_orden          = models.IntegerField(default=0)
    menu_activo         = models.BooleanField(default=True)
    menu_fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'menu'
    
    def __str__(self):
        return self.menu_titulo