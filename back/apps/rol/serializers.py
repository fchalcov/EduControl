from rest_framework import serializers
from apps.rol.models import Rol
from apps.menu.models import Menu

class RolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class RolSaveSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    rol_nombre = serializers.CharField()
    rol_descripcion = serializers.CharField(allow_blank=True, required=False)
    rol_activo = serializers.BooleanField()

class MenuRolListSerializer(serializers.ModelSerializer):

    titulo = serializers.CharField(source='menu_titulo')
    ruta = serializers.CharField(source='menu_ruta')
    icono = serializers.CharField(source='menu_icono')
    orden = serializers.IntegerField(source='menu_orden')
    checked = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            'id',
            'titulo', 
            'ruta', 
            'icono', 
            'orden',
            'checked', 
            'children'
        ]

    def get_checked(self, obj):
        role_menu_ids = self.context.get('role_menu_ids', set())
        return obj.id in role_menu_ids

    def get_children(self, obj):
        role_menu_ids = self.context.get('role_menu_ids', set())
        children = getattr(obj, 'children_list', [])

        return [
            {
                "id": c.id,
                "titulo": c.menu_titulo,
                "ruta": c.menu_ruta,
                "icono": c.menu_icono,
                "orden": c.menu_orden,
                "checked": c.id in role_menu_ids
            }
            for c in children
        ]