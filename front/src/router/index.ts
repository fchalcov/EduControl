import { createRouter, createWebHistory } from "vue-router";
import { useMenuStore } from "../store/menu";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: () => import("../modules/login/view/login.vue"),
  },
  {
    path: "/",
    component: () => import("../core/layout/AdminLayout.vue"),
    meta: { requiresAuth: true },
    children: [
      {
        path: "",
        name: "Home",
        component: () => import("../modules/home/view/home.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "dashboard",
        name: "Dashboard",
        component: () => import("../modules/dashboard/view/dashboard.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "permisos/permisos-rol",
        name: "Permisos de rol",
        component: () => import("../modules/permisos/view/permisos-rol.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "permisos/modulos",
        name: "Módulos del sistema",
        component: () => import("../modules/modulos/view/modulo.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "productos",
        name: "Productos",
        component: () => import("../modules/productos/view/producto.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "venta",
        name: "Venta",
        component: () => import("../modules/venta/view/venta.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "historial_venta",
        name: "Historial de Ventas",
        component: () => import("../modules/historial_venta/view/historial_venta.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "kardex",
        name: "Kardex",
        component: () => import("../modules/kardex/view/kardex.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "solicitud_pedido",
        name: "Solicitud de pedido",
        component: () => import("../modules/solicitud_pedido/view/solicitud_pedido.vue"),
        meta: { requiresAuth: true },
      },
    ],
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/login",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, _from, next) => {
  const auth = JSON.parse(localStorage.getItem("auth") || "{}");
  const token = auth.token;
  const isLogin = to.path === "/login";
  
  if (!token && !isLogin) {
    return next("/login");
  }
  
  if (token && isLogin) {
    return next("/");
  }
  
  if (token && to.meta.requiresAuth) {
    const menuStore = useMenuStore();
    
    if (!menuStore.loaded.value) {
      await menuStore.loadMenu();
    }
    
    if (to.path !== "/" && !menuStore.hasAccess(to.path)) {
      return next("/");
    }
  }
  
  next();
});

export default router;