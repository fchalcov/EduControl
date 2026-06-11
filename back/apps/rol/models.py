from django.db import models
from apps.menu.models import Menu


class Rol(models.Model):
    rol_nombre         = models.CharField(max_length=150, unique=True)
    rol_descripcion    = models.TextField(blank=True)
    rol_activo         = models.BooleanField(default=True)
    rol_fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rol'

    def __str__(self):
        return f"{self.rol_nombre} - {self.rol_descripcion}"


class RolMenu(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        db_table = 'rol_menu'
        unique_together = ('rol', 'menu')

    def __str__(self):
        return f"{self.rol.rol_nombre} - {self.menu.menu_titulo}"