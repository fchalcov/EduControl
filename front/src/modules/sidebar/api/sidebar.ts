import http from "../../../api/http";

export const list_menu_side_bar = () => {
    return http.get("/menu/list_menu_x_usuario/");
}