<template>
  <div class="h-dvh bg-gray-100 overflow-hidden">
    <!-- Sidebar -->
    <Sidebar
      :isCollapsed="isCollapsed"
      :isMobileMenuOpen="isMobileMenuOpen"
      :isMobile="isMobile"
      @closeMobile="closeMobileMenu"
      @toggleSidebar="toggleSidebar"
    />

    <!-- Contenedor principal -->
    <div
      :class="[
        'h-full flex flex-col min-w-0 transition-all duration-300',
        isMobile ? 'ml-0' : isCollapsed ? 'ml-20' : 'ml-64'
      ]"
    >
      <!-- Header -->
      <header class="h-16 bg-white border-b border-gray-200 flex-shrink-0 z-20">
        <div class="h-full flex items-center justify-between px-3 sm:px-4 lg:px-6 gap-3">
          <!-- Izquierda -->
          <div class="flex items-center gap-2 sm:gap-4 min-w-0">
            <!-- Botón móvil -->
            <button
              @click="toggleMobileMenu"
              class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>

            <!-- Botón desktop -->
            <button
              @click="toggleSidebar"
              class="hidden lg:flex p-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>

            <h1 class="text-base sm:text-lg lg:text-xl font-semibold text-gray-800 truncate">
              {{ pageTitle }}
            </h1>
          </div>

          <!-- Usuario -->
          <div class="relative flex-shrink-0">
            <button
              @click="showUserMenu = !showUserMenu"
              class="flex items-center gap-2 md:gap-3 px-2 md:px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div
                class="w-8 h-8 rounded-full bg-gray-900 flex items-center justify-center text-white text-sm font-medium"
              >
                {{ userInitial }}
              </div>

              <div class="hidden sm:block text-left max-w-40">
                <p class="text-sm font-medium text-gray-700 truncate">
                  {{ userName }}
                </p>
                <p class="text-xs text-gray-500 truncate">
                  {{ userEmail }}
                </p>
              </div>
            </button>

            <!-- Dropdown -->
            <div
              v-if="showUserMenu"
              class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-gray-200 py-1 z-40"
            >
              <div class="px-4 py-3 border-b border-gray-100">
                <p class="text-sm font-medium text-gray-900 truncate">
                  {{ userName }}
                </p>
                <p class="text-xs text-gray-500 truncate">
                  {{ userEmail }}
                </p>
              </div>

              <button
                @click="logout"
                class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
              >
                Cerrar sesión
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Contenido -->
      <main class="flex-1 min-w-0 overflow-y-auto overflow-x-hidden bg-gray-100">
        
          <router-view />
        
      </main>
    </div>
  </div>
</template>

<script setup>
import Sidebar from "../../modules/sidebar/view/sidebar.vue";
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

const isCollapsed = ref(false);
const isMobileMenuOpen = ref(false);
const showUserMenu = ref(false);
const isMobile = ref(false);

/* USER */
const auth = JSON.parse(localStorage.getItem("auth") || "{}");
const user = auth.user || {};

const userName = user.first_name || "Usuario";
const userEmail = user.email || "--";

const userInitial = computed(() =>
  user.first_name ? user.first_name.charAt(0).toUpperCase() : "U"
);

/* PAGE TITLE */
const pageTitle = computed(() => {
  const name = route.name;

  if (!name || route.path === "/") {
    return "Bienvenido";
  }

  return name;
});

/* FUNCIONES */
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
};

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

const logout = () => {
  localStorage.clear();
  router.push("/login");
};

/* RESPONSIVE */
const checkMobile = () => {
  isMobile.value = window.innerWidth < 1024;

  if (!isMobile.value) {
    closeMobileMenu();
  }
};

watch(
  () => route.path,
  () => {
    showUserMenu.value = false;

    if (isMobile.value) {
      closeMobileMenu();
    }
  }
);

onMounted(() => {
  checkMobile();
  window.addEventListener("resize", checkMobile);
});

onUnmounted(() => {
  window.removeEventListener("resize", checkMobile);
});
</script>