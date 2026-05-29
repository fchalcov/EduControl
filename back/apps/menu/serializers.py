from rest_framework import serializers
from .models import Menu

class MenuListSerializer(serializers.ModelSerializer):

    titulo = serializers.CharField(source='menu_titulo')
    ruta = serializers.CharField(source='menu_ruta')
    icono = serializers.CharField(source='menu_icono')
    orden = serializers.IntegerField(source='menu_orden')
    activo = serializers.BooleanField(source='menu_activo')
    padre_id = serializers.IntegerField(source='menu_padre_id')

    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            'id',
            'titulo',
            'ruta',
            'icono',
            'orden',
            'activo',
            'padre_id',
            'children'
        ]

    def get_children(self, obj):
        children = getattr(obj, 'children_list', [])
        return [
            {
                "id": c.id,
                "titulo": c.menu_titulo,
                "ruta": c.menu_ruta,
                "icono": c.menu_icono,
                "orden": c.menu_orden,
                "activo": c.menu_activo,
                "padre_id": c.menu_padre_id
            }
            for c in children
        ]
    
class MenuSaveSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    menu_titulo = serializers.CharField(required=True, allow_blank=False)
    menu_ruta = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    menu_icono = serializers.CharField(required=False, allow_null=True, default='ListBulletIcon')
    menu_orden = serializers.IntegerField(required=False, default=0, allow_null=True, min_value=0)
    menu_activo = serializers.BooleanField()
    menu_padre_id = serializers.IntegerField(required=False, allow_null=True, default=None)