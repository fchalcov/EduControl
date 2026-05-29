import { ref } from "vue";
import { list_menu_side_bar } from "../modules/sidebar/api/sidebar.ts";

const menuItems = ref([]);
const loaded = ref(false);

export const useMenuStore = () => {

  const loadMenu = async () => {
    if (loaded.value) return;
    try {
      const res = await list_menu_side_bar();
      menuItems.value = res.data;
      loaded.value = true;
    } catch (error) {
      console.error("Error cargando menú", error);
    }
  };

  return {
    menuItems,
    loadMenu,
  };
};