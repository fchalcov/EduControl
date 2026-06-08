<template>
  <!-- Overlay móvil -->
  <div
    v-if="isMobileMenuOpen"
    @click="$emit('closeMobile')"
    class="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden transition-opacity duration-300"
  ></div>

  <!-- Sidebar -->
  <aside
    :class="[
      'fixed left-0 top-0 h-full bg-white transition-all duration-300 z-30 shadow-xl',
      isCollapsed ? 'w-20' : 'w-64',
      isMobileMenuOpen
        ? 'translate-x-0'
        : '-translate-x-full lg:translate-x-0',
    ]"
  >
    <!-- ========== LOGO / HEADER ========== -->
    <div :class="[
      'flex items-center justify-center border-b border-gray-200 mb-2',
      !isCollapsed ? 'h-32 md:h-36 lg:h-44' : 'h-14 md:h-16 lg:h-16'
    ]">
      <div v-if="!isCollapsed" class="flex items-center gap-2 px-3">
        <img src="/logo_1.png" alt="Logo Micali" class="h-16 md:h-20 lg:h-28 w-auto"/>
      </div>
      <div v-else class="flex justify-center w-full">
        <img src="/logo_1.png" alt="Logo" class="h-7 md:h-8 lg:h-9 w-auto rounded-lg" />
      </div>
    </div>

    <!-- Menú -->
    <nav class="mt-2 px-2">
      <div v-for="item in menuItems" :key="item.id">

        <!-- ITEM -->
        <div
          @click="
            item.children && item.children.length
              ? toggleMenu(item.id)
              : navigate(item.ruta)
          "
          :class="[
            'flex items-center px-3 py-3 mb-1 rounded-lg cursor-pointer transition-all',
            isActive(item.ruta)
              ? 'bg-gray-900 text-white shadow-md'
              : 'text-gray-700 hover:bg-gray-300 hover:text-gray-600',
          ]"
        >
          <component
            v-if="Icons[item.icono]"
            :is="Icons[item.icono]"
            class="w-5 h-5"
          />

          <span v-if="!isCollapsed" class="ml-3 text-xs font-medium flex-1">
            {{ item.titulo }}
          </span>

          <svg
            v-if="item.children && item.children.length && !isCollapsed"
            :class="[
              'w-4 h-4 transition-transform text-gray-500',
              openMenus[item.id] ? 'rotate-90' : '',
            ]"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5l7 7-7 7"/>
          </svg>
        </div>

        <!-- SUBMENU -->
        <div
          v-if="item.children && openMenus[item.id] && !isCollapsed"
          class="ml-6"
        >
          <div
            v-for="child in item.children"
            :key="child.id"
            @click="navigate(child.ruta)"
            :class="[
              'flex items-center px-3 py-3 mb-1 rounded-lg cursor-pointer transition-all text-xs font-medium',
              isActive(child.ruta)
                ? 'bg-gray-900 text-white shadow-md'
                : 'text-gray-700 hover:bg-gray-300 hover:text-gray-600',
            ]"
          >
            <component
              v-if="Icons[child.icono]"
              :is="Icons[child.icono]"
              class="w-5 h-5"
            />
            <span class="ml-3">{{ child.titulo }}</span>
          </div>
        </div>

      </div>
    </nav>

    <!-- BOTÓN COLAPSAR -->
    <button
      v-if="!isMobile"
      @click="$emit('toggleSidebar')"
      class="absolute bottom-4 left-1/2 -translate-x-1/2 p-2 rounded-lg bg-gray-200 text-gray-600 hover:bg-gray-300 transition-all"
    >
      <svg
        v-if="!isCollapsed"
        class="w-4 h-4"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M15 19l-7-7 7-7"/>
      </svg>

      <svg
        v-else
        class="w-4 h-4"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M9 5l7 7-7 7"/>
      </svg>
    </button>
  </aside>
</template>

<script setup>
import * as Icons from "@heroicons/vue/24/outline";
import { ref, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useMenuStore } from "../../../store/menu.ts";

/* PROPS */
defineProps({
  isCollapsed: Boolean,
  isMobileMenuOpen: Boolean,
  isMobile: Boolean,
});

/* EMITS */
defineEmits(["closeMobile", "toggleSidebar"]);

/* ROUTER */
const router = useRouter();
const route = useRoute();

/* STORE */
const { menuItems, loadMenu } = useMenuStore();

/* STATE */
const openMenus = ref({});

/* NORMALIZAR RUTA */
const normalizePath = (path) => {
  if (!path) return null;
  return path.startsWith("/") ? path : "/" + path;
};

/* NAVIGATE */
const navigate = (path) => {
  const finalPath = normalizePath(path);
  if (!finalPath) return;
  router.push(finalPath);
};

/* ACTIVE */
const isActive = (path) => {
  const finalPath = normalizePath(path);
  if (!finalPath) return false;
  return route.path.startsWith(finalPath);
};

/* TOGGLE */
const toggleMenu = (id) => {
  openMenus.value[id] = !openMenus.value[id];
};

/* ABRIR MENÚ ACTIVO */
const openActiveMenu = () => {
  const currentPath = route.path;

  menuItems.value.forEach((item) => {
    if (item.children && item.children.length) {
      const found = item.children.find((child) =>
        currentPath.startsWith(normalizePath(child.ruta))
      );

      if (found) {
        openMenus.value[item.id] = true;
      }
    }
  });
};

/* WATCH ROUTE */
watch(() => route.path, () => {
  openActiveMenu();
});

/* INIT */
onMounted(async () => {
  console.log("Sidebar montado");
  await loadMenu();
  openActiveMenu();
});
</script>