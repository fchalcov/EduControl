import http from "../../../api/http";

export const list_menu = () => {
  return http.get("/menu/list_menu/");
};

export const save_menu = (data: any) => {
  return http.post("/menu/save_menu/", data);
};