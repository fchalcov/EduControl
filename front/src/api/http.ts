import axios from "axios";
import Swal from "sweetalert2";
import router from "../router";

/* =========================
   STATE
========================= */

let isRefreshing = false;
let failedQueue: any[] = [];

/* =========================
   HELPERS
========================= */

const getAuth = () => {
  return JSON.parse(localStorage.getItem("auth") || "{}");
};

const setAuth = (auth: any) => {
  localStorage.setItem("auth", JSON.stringify(auth));
};

const clearAuth = () => {
  localStorage.clear();
};

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) prom.reject(error);
    else prom.resolve(token);
  });

  failedQueue = [];
};

/* =========================
   API BASE URL
========================= */

const API_BASE_URL = (
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "");

/* =========================
   AXIOS INSTANCE
========================= */

const http = axios.create({
  baseURL: `${API_BASE_URL}/`,
  headers: {
    "Content-Type": "application/json",
  },
});

/* =========================
   REQUEST INTERCEPTOR
========================= */

http.interceptors.request.use(
  (config) => {
    const auth = getAuth();

    if (auth?.token) {
      config.headers.Authorization = `Bearer ${auth.token}`;
    }

    return config;
  },
  (error) => Promise.reject(error),
);

/* =========================
   RESPONSE INTERCEPTOR
========================= */

http.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;
    const status = error.response?.status;

    const auth = getAuth();

    /* =========================
       🚫 IGNORAR LOGIN (CLAVE)
    ========================= */
    if (originalRequest.url.includes("/login")) {
      return Promise.reject(error);
    }

    /* =========================
       🔐 TOKEN EXPIRADO
    ========================= */
    if (
      status === 401 &&
      !originalRequest._retry &&
      auth?.refresh
    ) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return http(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const res = await axios.post(
          `${API_BASE_URL}/api/token/refresh/`,
          {
            refresh: auth.refresh,
          }
        );

        const newToken = res.data.access;

        auth.token = newToken;
        setAuth(auth);

        processQueue(null, newToken);

        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return http(originalRequest);

      } catch (err) {
        processQueue(err, null);

        clearAuth();

        await Swal.fire({
          icon: "error",
          title: "Sesión expirada",
          text: "Inicia sesión nuevamente",
          confirmButtonText: "OK",
          allowOutsideClick: false,
        });

        router.replace("/login");

        return Promise.reject(err);

      } finally {
        isRefreshing = false;
      }
    }

    /* =========================
       ⚠️ OTROS ERRORES
    ========================= */

    if (status === 403) {
      console.warn("Acceso denegado");
    }

    if (status === 500) {
      console.error("Error del servidor");
    }

    return Promise.reject(error);
  },
);

export default http;