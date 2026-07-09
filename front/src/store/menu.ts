// store/menu.ts
import { ref } from "vue";
import { list_menu_side_bar } from "../modules/sidebar/api/sidebar.ts";

interface MenuItem {
  id: number;
  titulo: string;
  ruta: string;
  icono?: string;
  children?: MenuItem[];
}

const menuItems = ref<MenuItem[]>([]);
const allowedRoutes = ref<string[]>([]);
const loaded = ref(false);

export const useMenuStore = () => {
  
  const extractRoutes = (menus: MenuItem[]): string[] => {
    const routes: string[] = [];
    
    const extract = (items: MenuItem[]) => {
      for (const item of items) {
        if (item.ruta) {
          const normalizedPath = item.ruta.startsWith('/') ? item.ruta : '/' + item.ruta;
          routes.push(normalizedPath);
        }
        if (item.children && item.children.length > 0) {
          extract(item.children);
        }
      }
    };
    
    extract(menus);
    return routes;
  };

  const loadMenu = async (): Promise<void> => {
    if (loaded.value) return;
    
    try {
      const res = await list_menu_side_bar();
      menuItems.value = res.data;
      
      // Extraer rutas del backend
      const backendRoutes = extractRoutes(res.data);

      if (!backendRoutes.includes('/')) {
        allowedRoutes.value = ['/', ...backendRoutes];
      } else {
        allowedRoutes.value = backendRoutes;
      }     
      loaded.value = true;
    } catch (error) {
      throw error;
    }
  };

  // Verificar si una ruta tiene acceso
  const hasAccess = (path: string): boolean => {
    const normalizedPath = path.startsWith('/') ? path : '/' + path;
    
    if (normalizedPath === '/') {
      return true;
    }
    
    const hasPermission = allowedRoutes.value.some(route => normalizedPath === route);
    return hasPermission;
  };

  const clearMenu = (): void => {
    menuItems.value = [];
    allowedRoutes.value = [];
    loaded.value = false;
  };

  return {
    menuItems,
    allowedRoutes,
    loaded,
    loadMenu,
    hasAccess,
    clearMenu,
  };
};