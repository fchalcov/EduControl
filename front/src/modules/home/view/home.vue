<!-- modules/home/view/home.vue -->
<template>
  <div class="flex items-center justify-center w-full" style="min-height: calc(100vh - 120px);">
    <div class="max-w-2xl w-full text-center px-4 py-8 md:px-8">
      <!-- Animación de bienvenida -->
      <div class="mb-1 md:mb-2">
        <div class="inline-flex p-3 md:p-4 rounded-full mb-0 md:mb-0">
            <img 
            src="/logo_3.png"
            alt="Micali Market" 
            class="w-28 h-28 sm:w-32 sm:h-32 md:w-40 md:h-40 object-contain drop-shadow-lg hover:scale-105 transition-transform duration-300"
            />
        </div>
      </div>
      
      <p class="text-base md:text-xl text-gray-600 mb-2 md:mb-2">
        Sistema de Gestión de Ventas
      </p>
      
      <div class="flex items-center justify-center gap-2 mb-6 md:mb-8">
        <span class="w-8 md:w-12 h-0.5 bg-rose-300"></span>
        <span class="w-1.5 h-1.5 md:w-2 md:h-2 bg-rose-500 rounded-full"></span>
        <span class="w-8 md:w-12 h-0.5 bg-rose-300"></span>
      </div>
      
      <!-- Mensaje de bienvenida - Responsivo -->
      <div class="bg-blue-50 rounded-lg p-4 md:p-6 mb-6 md:mb-8">
        <p class="text-base md:text-lg text-gray-700 mb-1 md:mb-2">
          ¡Bienvenido{{ userName ? ' ' + userName : '' }}!
        </p>
        <p class="text-sm md:text-base text-gray-600">
          Selecciona un módulo del menú lateral para comenzar a gestionar tus ventas
        </p>
      </div>
      
      <!-- Módulos rápidos - Grid responsivo -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4 mt-6 md:mt-8">
        <div class="bg-white rounded-lg p-3 md:p-4 border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
             @click="navigateTo('venta')">
          <div class="text-green-600 mb-2">
            <svg class="w-6 h-6 md:w-8 md:h-8 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" 
                d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-1.5 6M17 13l1.5 6M9 21h6M12 15v6" />
            </svg>
          </div>
          <h3 class="font-semibold text-gray-800 text-sm md:text-base">Nueva Venta</h3>
          <p class="text-xs md:text-sm text-gray-500 mt-1">Gestionar Venta</p>
        </div>
        
        <div class="bg-white rounded-lg p-3 md:p-4 border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
             @click="navigateTo('productos')">
          <div class="text-blue-600 mb-2">
            <svg class="w-6 h-6 md:w-8 md:h-8 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" 
                d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
          </div>
          <h3 class="font-semibold text-gray-800 text-sm md:text-base">Productos</h3>
          <p class="text-xs md:text-sm text-gray-500 mt-1">Gestionar Inventario</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { computed } from 'vue';

const router = useRouter();

// Obtener nombre del usuario si está disponible
const auth = JSON.parse(localStorage.getItem("auth") || "{}");
const user = auth.user || {};
const userName = computed(() => user.first_name || "");

const navigateTo = (path) => {
  router.push(`/${path}`);
};
</script>