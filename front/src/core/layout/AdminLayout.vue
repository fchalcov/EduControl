<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Sidebar -->
    <Sidebar :isCollapsed="isCollapsed" :isMobileMenuOpen="isMobileMenuOpen" :isMobile="isMobile"
      @closeMobile="closeMobileMenu" @toggleSidebar="toggleSidebar" />

    <!-- CONTENIDO -->
    <div :class="[
      'transition-all duration-300',
      isMobile ? 'ml-0' : isCollapsed ? 'ml-20' : 'ml-64',
    ]">
      <!-- HEADER -->
      <header class="bg-white shadow-sm sticky top-0 z-20">
        <div class="flex justify-between items-center px-4 md:px-6 h-16">
          <!-- IZQUIERDA -->
          <div class="flex items-center gap-4">
            <!-- MOBILE -->
            <button @click="toggleMobileMenu"
              class="lg:hidden text-gray-600 p-2 hover:bg-gray-100 rounded-lg transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>

            <!-- DESKTOP -->
            <button @click="toggleSidebar"
              class="hidden lg:block text-gray-600 hover:bg-gray-100 p-2 rounded-lg transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>

            <h1 class="text-lg md:text-xl font-semibold text-gray-800 truncate">
              {{ pageTitle }}
            </h1>
          </div>

          <!-- USUARIO -->
          <div class="relative">
            <button @click="showUserMenu = !showUserMenu"
              class="flex items-center gap-2 md:gap-3 hover:bg-gray-50 px-2 md:px-3 py-2 rounded-lg transition-colors">
              <div
                class="w-8 h-8 rounded-full bg-gradient-to-r from-[#1e3c72] to-[#2a5298] flex items-center justify-center text-white text-sm font-medium">
                {{ userInitial }}
              </div>

              <div class="hidden sm:block text-left">
                <p class="text-sm font-medium text-gray-700">{{ userName }}</p>
                <p class="text-xs text-gray-500">{{ userEmail }}</p>
              </div>
            </button>

            <!-- DROPDOWN -->
            <div v-if="showUserMenu"
              class="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-100 py-1 z-30">
              <div class="px-4 py-3 border-b border-gray-100">
                <p class="text-sm font-medium text-gray-900">{{ userName }}</p>
                <p class="text-xs text-gray-500 truncate">{{ userEmail }}</p>
              </div>

              <button @click="logout"
                class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors">
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- CONTENIDO -->
      <main class="p-4 md:p-6 bg-gray-100 min-h-[calc(100vh-4rem)] flex flex-col">
        <div class="flex-1 flex flex-col bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="flex-1 overflow-auto p-4 md:p-6">
            <div class="flex-1 overflow-auto p-4 md:p-6">
              <router-view />
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
<script setup>
import Sidebar from "../../modules/sidebar/view/sidebar.vue";
import { ref, computed, onMounted, onUnmounted } from "vue";
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
  user.first_name ? user.first_name.charAt(0).toUpperCase() : "U",
);

/* PAGE TITLE */
// const pageTitle = computed(() => route.name || "Panel de Control");

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

/* MOBILE */
const checkMobile = () => {
  isMobile.value = window.innerWidth < 1024;

  if (!isMobile.value) closeMobileMenu();
};

onMounted(() => {
  checkMobile();
  window.addEventListener("resize", checkMobile);
});

onUnmounted(() => {
  window.removeEventListener("resize", checkMobile);
});
</script>
