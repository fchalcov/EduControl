<!-- BarcodeScanner.vue - Versión simplificada sin librerías externas -->
<template>
  <div v-if="visible" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="fixed inset-0 bg-black/90 backdrop-blur-sm" @click="cerrar"></div>
    
    <div class="flex min-h-full items-center justify-center p-4">
      <div class="relative bg-white w-full max-w-2xl rounded-xl shadow-2xl">
        <div class="p-6">
          <h3 class="text-lg font-semibold mb-4">Escanear Código de Barras</h3>
          
          <!-- Simulador de escáner para pruebas -->
          <div class="bg-gray-100 rounded-lg p-8 text-center">
            <p class="text-gray-600 mb-4">📷 Modo de prueba</p>
            <input 
              v-model="codigoSimulado"
              type="text"
              placeholder="Ingresa código manualmente"
              class="w-full px-4 py-2 border rounded-lg mb-4"
            />
            <button 
              @click="simularEscaneo"
              class="px-6 py-2 bg-blue-600 text-white rounded-lg">
              Simular Escaneo
            </button>
          </div>
          
          <div class="mt-4 flex justify-end">
            <button @click="cerrar" class="px-4 py-2 text-gray-600">Cancelar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BarcodeScanner",
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      codigoSimulado: ""
    };
  },
  methods: {
    simularEscaneo() {
      if (this.codigoSimulado) {
        this.$emit("scanned", this.codigoSimulado);
        this.cerrar();
      }
    },
    cerrar() {
      this.$emit("update:visible", false);
    }
  }
};
</script>