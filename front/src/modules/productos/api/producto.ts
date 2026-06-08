import http from "../../../api/http";

export const list_producto = (params = {}) => {
  return http.get("/producto/producto_list/", { params });
};

export const get_producto = (id: number) => {
  return http.get(`/producto/producto_detail/${id}/`);
};

export const create_producto = (data: any) => {
  return http.post("/producto/producto_create/", data);
};  

export const update_producto = (id: number, data: any) => {
  return http.put(`/producto/producto_update/${id}/`, data);
};

export const delete_producto = (id: number) => {
  return http.delete(`/producto/producto_delete/${id}/`);  
};

export const importar_productos_excel = (file: File) => {
  const formData = new FormData();
  formData.append('archivo', file);
  return http.post('/producto/producto_importar_excel/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};