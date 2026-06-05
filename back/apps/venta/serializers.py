from decimal import Decimal

from rest_framework import serializers

from .models import Venta, VentaPago, DetalleVenta


class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = [
            "id_detalle",
            "id_venta",
            "descripcion_producto",
            "codigo_barra",
            "cantidad_venta",
            "precio_venta",
            "sub_total_venta",
            "estado_venta",
        ]


class VentaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaPago
        fields = [
            "id_pago",
            "id_venta",
            "forma_pago",
            "monto_pagar",
            "efectivo_recibido",
            "efectivo_vuelto",
        ]


class VentaSerializer(serializers.ModelSerializer):
    pagos = VentaPagoSerializer(many=True, read_only=True)
    detalles = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = [
            "id_venta",
            "correlativo_venta",
            "fecha_venta",
            "id_usuario_venta",
            "total_venta",
            "estado_venta",
            "pagos",
            "detalles",
        ]


class DetalleVentaCreateSerializer(serializers.Serializer):
    descripcion_producto = serializers.CharField(max_length=255)
    codigo_barra = serializers.CharField(
        max_length=100, required=False, allow_blank=True, default=""
    )
    cantidad_venta = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("0.01")
    )
    precio_venta = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("0")
    )
    sub_total_venta = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("0")
    )


class VentaPagoCreateSerializer(serializers.Serializer):
    forma_pago = serializers.IntegerField(min_value=1, max_value=4)
    monto_pagar = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("0.01")
    )
    efectivo_recibido = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    efectivo_vuelto = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )


class VentaCreateSerializer(serializers.Serializer):
    id_usuario_venta = serializers.IntegerField(required=False)
    detalles = DetalleVentaCreateSerializer(many=True)
    pagos = VentaPagoCreateSerializer(many=True)

    def validate_detalles(self, value):
        if not value:
            raise serializers.ValidationError(
                "Debe incluir al menos un producto en la venta."
            )
        return value

    def validate_pagos(self, value):
        if not value:
            raise serializers.ValidationError(
                "Debe incluir al menos un método de pago."
            )
        return value

    def validate(self, data):
        total_detalles = sum(d["sub_total_venta"] for d in data["detalles"])
        total_pagos = sum(p["monto_pagar"] for p in data["pagos"])

        if total_detalles != total_pagos:
            raise serializers.ValidationError(
                "La suma de los pagos debe coincidir con el total de la venta."
            )

        for detalle in data["detalles"]:
            esperado = detalle["cantidad_venta"] * detalle["precio_venta"]
            if abs(detalle["sub_total_venta"] - esperado) > Decimal("0.01"):
                raise serializers.ValidationError(
                    "El subtotal de un producto no coincide con cantidad × precio."
                )

        return data
