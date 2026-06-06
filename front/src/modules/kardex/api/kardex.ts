import http from "../../../api/http";

export const list_tipo_movimientos = () => {
  return http.get("/kardex/tipo_movimiento_list/");
}

export const list_kardex = (params = {}) => {
  return http.get("/kardex/kardex_list/", { params });
}