import { createRouter, createWebHistory } from "vue-router";

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
        redirect: "/dashboard",
      },
      {
        path: "dashboard",
        name: "Dashboard",
        component: () => import("../modules/dashboard/view/dashboard.vue"),
      },
      {
        path: "permisos/permisos-rol",
        name: "Permisos de rol",
        component: () => import("../modules/permisos/view/permisos-rol.vue"),
      },
      {
        path: "permisos/modulos",
        name: "Módulos del sistema",
        component: () => import("../modules/modulos/view/modulo.vue"),
      },
      {
        path: "productos",
        name: "Productos",
        component: () => import("../modules/productos/view/producto.vue"),
      },
      {
        path: "venta",
        name: "Venta",
        component: () => import("../modules/venta/view/venta.vue"),
      },
      {
        path: "historial_venta",
        name: "Historial de Ventas",
        component: () => import("../modules/historial_venta/view/historial_venta.vue"),
      },
      {
        path: "kardex",
        name: "Kardex",
        component: () => import("../modules/kardex/view/kardex.vue"),
      },
      {
        path: "solicitud_pedido",
        name: "Solicitud de pedido",
        component: () => import("../modules/solicitud_pedido/view/solicitud_pedido.vue"),
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

router.beforeEach((to, _from, next) => {
  const auth = JSON.parse(localStorage.getItem("auth") || "{}");
  const token = auth.token;
  const isLogin = to.path === "/login";
  if (!token && !isLogin) {
    return next("/login");
  }
  if (token && isLogin) {
    return next("/dashboard");
  }
  next();
});

export default router;
