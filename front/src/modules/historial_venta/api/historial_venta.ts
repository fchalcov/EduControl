import http from "../../../api/http";

export const list_historial_ventas = (params = {}) => {
  return http.get("/venta/venta_list/", { params });
};

export const get_historial_venta = (id: number) => {
  return http.get(`/venta/venta_detail/${id}/`);
};
