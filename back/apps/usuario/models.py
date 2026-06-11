from django.db import models
from django.contrib.auth.models import User
from apps.rol.models import Rol
from apps.menu.models import Menu


class UsuarioRol(models.Model):
    usuario            = models.OneToOneField(User, on_delete=models.CASCADE)
    usuario_rol        = models.ForeignKey(Rol, on_delete=models.CASCADE)
    rol_fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuario_rol'

    def __str__(self):
        return self.usuario.username

class UsuarioMenu(models.Model):
    usuario     = models.ForeignKey(User, on_delete=models.CASCADE)
    menu        = models.ForeignKey(Menu, on_delete=models.CASCADE)
    permiso_ver = models.BooleanField(default=True)

    class Meta:
        db_table = 'usuario_menu'
        unique_together = ('usuario', 'menu')

    def __str__(self):
        return f"{self.usuario.username} - {self.menu.menu_titulo}"