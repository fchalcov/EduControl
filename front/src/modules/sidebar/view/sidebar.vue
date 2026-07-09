<template>
  <!-- Overlay móvil -->
  <div
    v-if="isMobileMenuOpen"
    @click="emit('closeMobile')"
    class="fixed inset-0 bg-black/50 z-30 lg:hidden"
  ></div>

  <!-- Sidebar -->
  <aside
    :class="[
      'fixed left-0 top-0 h-dvh bg-white border-r border-gray-200 transition-all duration-300 z-40 shadow-lg lg:shadow-none',
      isMobile ? 'w-72 max-w-[85vw]' : isCollapsed ? 'w-20' : 'w-64',
      isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
    ]"
  >
    <!-- Logo -->
    <div
      :class="[
        'flex items-center justify-center border-b border-gray-200 px-3',
        isMobile || !isCollapsed ? 'h-24 lg:h-32' : 'h-16'
      ]"
    >
      <img
        src="/logo_1.png"
        alt="Logo Micali"
        :class="[
          'w-auto object-contain transition-all duration-300',
          isMobile || !isCollapsed ? 'h-16 lg:h-24' : 'h-8'
        ]"
      />
    </div>

    <!-- Menú -->
    <nav class="h-[calc(100dvh-8rem)] overflow-y-auto px-2 py-3">
      <div v-for="item in menuItems" :key="item.id">
        <!-- Item principal -->
        <button
          @click="
            item.children && item.children.length
              ? toggleMenu(item.id)
              : navigate(item.ruta)
          "
          :class="[
            'w-full flex items-center rounded-lg px-3 py-3 mb-1 transition-all text-left',
            isActive(item.ruta)
              ? 'bg-gray-900 text-white shadow-sm'
              : 'text-gray-700 hover:bg-gray-100',
          ]"
        >
          <component
            v-if="Icons[item.icono]"
            :is="Icons[item.icono]"
            class="w-5 h-5 flex-shrink-0"
          />

          <span
            v-if="isMobile || !isCollapsed"
            class="ml-3 text-xs font-medium flex-1 truncate"
          >
            {{ item.titulo }}
          </span>

          <svg
            v-if="item.children && item.children.length && (isMobile || !isCollapsed)"
            :class="[
              'w-4 h-4 transition-transform flex-shrink-0',
              openMenus[item.id] ? 'rotate-90' : ''
            ]"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </button>

        <!-- Submenú -->
        <div
          v-if="item.children && openMenus[item.id] && (isMobile || !isCollapsed)"
          class="ml-4 border-l border-gray-200 pl-2 mb-1"
        >
          <button
            v-for="child in item.children"
            :key="child.id"
            @click="navigate(child.ruta)"
            :class="[
              'w-full flex items-center rounded-lg px-3 py-2.5 mb-1 transition-all text-left',
              isActive(child.ruta)
                ? 'bg-gray-900 text-white shadow-sm'
                : 'text-gray-600 hover:bg-gray-100',
            ]"
          >
            <component
              v-if="Icons[child.icono]"
              :is="Icons[child.icono]"
              class="w-4 h-4 flex-shrink-0"
            />

            <span class="ml-3 text-xs font-medium truncate">
              {{ child.titulo }}
            </span>
          </button>
        </div>
      </div>
    </nav>

    <!-- Botón colapsar desktop -->
    <button
      v-if="!isMobile"
      @click="emit('toggleSidebar')"
      class="absolute bottom-4 left-1/2 -translate-x-1/2 p-2 rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200 transition-all"
    >
      <svg
        v-if="!isCollapsed"
        class="w-4 h-4"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15 19l-7-7 7-7"
        />
      </svg>

      <svg
        v-else
        class="w-4 h-4"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 5l7 7-7 7"
        />
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
const props = defineProps({
  isCollapsed: Boolean,
  isMobileMenuOpen: Boolean,
  isMobile: Boolean,
});

/* EMITS */
const emit = defineEmits(["closeMobile", "toggleSidebar"]);

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
const navigate = async (path) => {
  const finalPath = normalizePath(path);

  if (!finalPath) return;

  await router.push(finalPath);

  if (props.isMobile) {
    emit("closeMobile");
  }
};

/* ACTIVE */
const isActive = (path) => {
  const finalPath = normalizePath(path);

  if (!finalPath) return false;

  return route.path === finalPath || route.path.startsWith(finalPath + "/");
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
      const found = item.children.find((child) => {
        const childPath = normalizePath(child.ruta);

        return (
          childPath &&
          (currentPath === childPath || currentPath.startsWith(childPath + "/"))
        );
      });

      if (found) {
        openMenus.value[item.id] = true;
      }
    }
  });
};

/* WATCH ROUTE */
watch(
  () => route.path,
  () => {
    openActiveMenu();
  }
);

/* INIT */
onMounted(async () => {
  await loadMenu();
  openActiveMenu();
});
</script>