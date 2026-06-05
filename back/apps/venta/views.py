from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.producto.models import Producto

from .models import Venta, VentaPago, DetalleVenta
from .serializers import VentaCreateSerializer


def _descontar_stock(detalles):
    for detalle in detalles:
        codigo = (detalle.get("codigo_barra") or "").strip()
        if not codigo:
            continue

        producto = Producto.objects.select_for_update().filter(
            codigo_barra=codigo,
            estado=True,
        ).first()

        if not producto:
            continue

        cantidad = int(detalle["cantidad_venta"])
        if producto.cantidad_producto < cantidad:
            raise ValueError(
                f"Stock insuficiente para '{producto.nombre_producto}'. "
                f"Disponible: {producto.cantidad_producto}, solicitado: {cantidad}."
            )

        producto.cantidad_producto -= cantidad
        producto.save(update_fields=["cantidad_producto", "fecha_actualizacion"])


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def crear_venta(request):
    serializer = VentaCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    try:
        _descontar_stock(data["detalles"])
    except ValueError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    ultima_venta = Venta.objects.select_for_update().order_by("-id_venta").first()
    nuevo_correlativo = (
        f"V-{ultima_venta.id_venta + 1:06d}" if ultima_venta else "V-000001"
    )

    total_venta = sum(d["sub_total_venta"] for d in data["detalles"])

    venta = Venta.objects.create(
        correlativo_venta=nuevo_correlativo,
        fecha_venta=timezone.now(),
        id_usuario_venta=request.user.id,
        total_venta=total_venta,
        estado_venta=1,
    )

    for detalle_data in data["detalles"]:
        DetalleVenta.objects.create(
            id_venta=venta.id_venta,
            descripcion_producto=detalle_data["descripcion_producto"],
            codigo_barra=detalle_data.get("codigo_barra", ""),
            cantidad_venta=detalle_data["cantidad_venta"],
            precio_venta=detalle_data["precio_venta"],
            sub_total_venta=detalle_data["sub_total_venta"],
        )

    for pago_data in data["pagos"]:
        VentaPago.objects.create(
            id_venta=venta.id_venta,
            forma_pago=pago_data["forma_pago"],
            monto_pagar=pago_data["monto_pagar"],
            efectivo_recibido=pago_data.get("efectivo_recibido"),
            efectivo_vuelto=pago_data.get("efectivo_vuelto"),
        )

    return Response(
        {
            "success": True,
            "venta_id": venta.id_venta,
            "correlativo": venta.correlativo_venta,
            "message": "Venta registrada exitosamente",
        },
        status=status.HTTP_201_CREATED,
    )
