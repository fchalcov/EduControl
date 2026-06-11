import http from "../../../api/http";

export const create_venta = (data: any) => {
  return http.post("/venta/venta_create/", data);
};  

export const producto_list_x_codigo = (codigoBarra: string, estado?: string) => {
  const params: any = { codigo_barra: codigoBarra };
  if (estado) {
    params.estado = estado;
  }
  return http.get("/producto/producto_list_x_codigo/", { params });
};

export interface Venta {
    id_venta: number;
    correlativo_venta: string;
    fecha_venta: string;
    id_usuario_venta: number;
    total_venta: number;
    estado_venta: 1 | 2 | 3;
}

export interface VentaPago {
    id_pago: number;
    id_venta: number;
    forma_pago: 1 | 2 | 3 | 4;
    monto_pagar: number;
    efectivo_recibido?: number;
    efectivo_vuelto?: number;
    fecha_pago: string;
}

export interface DetalleVenta {
    id_detalle: number;
    id_venta: number;
    descripcion_producto: string;
    codigo_barra: string;
    cantidad_venta: number;
    precio_venta: number;
    sub_total_venta: number;
    estado_venta: 1 | 2 | 3;
}