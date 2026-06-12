<template>
  <!-- ✅ SOLO AGREGUE ESTOS 2 EVENTOS -->
  <div 
    @keydown="handleKeydown"
    @paste="handlePaste"
    class="h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col"
  >
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 px-4 sm:px-8 py-4 sm:py-6">
      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4 sm:gap-0">
        
        <!-- Logo y título -->
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center flex-shrink-0">
            <span class="text-white text-sm font-bold">V</span>
          </div>
          <div>
            <h1 class="text-base sm:text-xl font-semibold text-gray-800 tracking-tight">Venta</h1>
            <p class="text-xs text-gray-500 hidden sm:block">Punto de venta</p>
          </div>
        </div>
        
        <!-- Botón -->
        <div class="flex gap-3">
          <button @click="openProductModal"
            class="flex-1 sm:flex-none px-4 sm:px-5 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 transition-colors flex items-center justify-center gap-2">
            Buscar Producto
          </button>
        </div>
      </div>
    </header>

    <!-- Contenido Principal: Carrito + Pago en una sola vista -->
    <main class="px-8 py-6 h-[calc(100vh-120px)]">
      <div class="w-full h-full mx-auto grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        
        <!-- Columna Izquierda y Central: Carrito de compras (2/3 del espacio) -->
        <div class="lg:col-span-2 flex flex-col bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden h-full">
          
          <!-- Header del carrito -->
          <div class="px-4 sm:px-5 py-3 border-b border-gray-200 bg-gray-50 flex-shrink-0">
            <div class="flex justify-between items-center">
              <h2 class="text-sm font-semibold text-gray-700 flex items-center gap-2">
                <span class="w-1 h-4 bg-gray-900 rounded-full"></span>
                Carrito de compra
              </h2>
              <span class="text-xs sm:text-sm text-gray-500 bg-white px-2 sm:px-3 py-1 rounded-lg border border-gray-200">
                {{ cart.length }} {{ cart.length === 1 ? 'producto' : 'productos' }}
              </span>
            </div>
          </div>
          
          <!-- Lista de productos del carrito en formato TABLA -->
          <div class="flex-1 overflow-y-auto">
            <div v-if="cart.length === 0" class="text-center py-12 sm:py-16">
              <div class="w-16 h-16 sm:w-20 sm:h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
                <svg class="w-8 h-8 sm:w-10 sm:h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
              </div>
              <p class="text-gray-500 text-sm sm:text-base">Carrito vacío</p>
              <p class="text-xs text-gray-400 mt-1 sm:mt-2">Presione "Buscar producto" o use el escáner</p>
            </div>
            
            <div v-else class="overflow-x-auto">
              <table class="min-w-full text-sm">
                <thead class="bg-gray-50 sticky top-0">
                  <tr>
                    <th class="px-3 py-2 text-left text-xs font-medium text-gray-500">Código Barra</th>
                    <th class="px-3 py-2 text-left text-xs font-medium text-gray-500">Producto</th>
                    <th class="px-3 py-2 text-left text-xs font-medium text-gray-500">Stock</th>
                    <th class="px-3 py-2 text-center text-xs font-medium text-gray-500">Cantidad</th>
                    <th class="px-3 py-2 text-right text-xs font-medium text-gray-500">Precio Unit.</th>
                    <th class="px-3 py-2 text-right text-xs font-medium text-gray-500">Subtotal</th>
                    <th class="px-3 py-2 text-center text-xs font-medium text-gray-500">Acción</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr 
                    v-for="(item, index) in cart" 
                    :key="item.id"
                    class="hover:bg-gray-50 transition-colors text-sm"
                  >
                    <td class="px-3 py-2 text-xs text-gray-500">{{ item.codigo_barra || 'Sin código' }}</td>
                    <td class="px-3 py-2 text-sm text-gray-800">{{ item.nombre_producto }}</td>
                    <td class="px-3 py-2 text-xs text-gray-500">
                      <span :class="[
                        'text-xs px-1.5 py-0.5 rounded-full',
                        item.cantidad_producto <= 5 ? 'bg-yellow-100 text-yellow-700' : 'bg-gray-100 text-gray-600'
                      ]">
                        {{ item.cantidad_producto }}
                      </span>
                    </td>
                    <td class="px-3 py-2 text-center">
                      <div class="flex items-center justify-center gap-1">
                        <button 
                          @click="updateQuantity(index, -1)" 
                          class="w-6 h-6 rounded border border-gray-200 bg-white text-gray-600 hover:bg-gray-100 transition-colors text-sm font-medium flex items-center justify-center"
                        >
                          −
                        </button>
                        <span class="text-sm font-semibold text-gray-800 w-8 text-center">{{ item.quantity }}</span>
                        <button 
                          @click="updateQuantity(index, 1)" 
                          class="w-6 h-6 rounded border border-gray-200 bg-white text-gray-600 hover:bg-gray-100 transition-colors text-sm font-medium flex items-center justify-center"
                        >
                          +
                        </button>
                      </div>
                    </td>
                    <td class="px-3 py-2 text-right text-sm text-gray-600">{{ formatCurrency(item.precio_unitario) }}</td>
                    <td class="px-3 py-2 text-right text-sm font-bold text-gray-900">{{ formatCurrency(item.precio_unitario * item.quantity) }}</td>
                    <td class="px-3 py-2 text-center text-sm font-bold text-gray-900">
                      <button 
                        @click="removeFromCart(index)" 
                        class="px-2 py-1 text-xs bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50 transition-colors"
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Columna Derecha: Pago (1/3 del espacio) -->
        <div class="lg:col-span-1 flex flex-col bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden h-full">
          
          <!-- Header del pago - Fijo -->
          <div class="px-4 sm:px-5 py-3 border-b border-gray-200 bg-gray-50 flex-shrink-0">
            <h2 class="text-sm font-semibold text-gray-700 flex items-center gap-2">
              <span class="w-1 h-4 bg-gray-900 rounded-full"></span>
              Forma de pago
            </h2>
          </div>
          
          <!-- Contenido del pago -->
          <div class="flex-1 overflow-y-auto">
            <div class="p-4 sm:p-5 space-y-4">
              
              <!-- Métodos de pago -->
              <div class="grid grid-cols-2 gap-3">
                <button 
                  @click="togglePaymentMethod(PAYMENT_CODES.CASH)"
                  :class="[
                    'p-1 rounded-xl border-2 transition-all text-center',
                    selectedPaymentMethod === PAYMENT_CODES.CASH 
                      ? 'border-gray-800 bg-gray-800 text-white' 
                      : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                  ]"
                >
                  <p class="text-xs sm:text-sm font-medium mt-1">Efectivo</p>
                </button>
                
                <button 
                  @click="togglePaymentMethod(PAYMENT_CODES.YAPE)"
                  :class="[
                    'p-1 rounded-xl border-2 transition-all text-center',
                    selectedPaymentMethod === PAYMENT_CODES.YAPE 
                      ? 'border-gray-800 bg-gray-800 text-white' 
                      : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                  ]"
                >
                  <p class="text-xs sm:text-sm font-medium mt-1">Yape</p>
                </button>
              </div>
              
              <!-- Input de monto según método seleccionado -->
              <div v-if="selectedPaymentMethod && remainingBalance > 0">
                <label class="block text-xs sm:text-sm font-medium text-gray-600 mb-1">
                  {{ selectedPaymentMethod === PAYMENT_CODES.CASH ? 'Monto recibido' : 'Monto a pagar con Yape' }}
                </label>
                <input 
                  ref="cashInput"
                  :value="selectedPaymentMethod === PAYMENT_CODES.CASH ? cashAmountText : yapeAmountText"
                  @input="selectedPaymentMethod === PAYMENT_CODES.CASH ? updateCashAmount($event) : updateYapeAmount($event)"
                  @focus="onPaymentInputFocus"
                  @blur="onPaymentInputBlur"
                  type="number"
                  inputmode="decimal"
                  class="w-full px-3 py-1 border-2 border-gray-200 rounded-lg text-base sm:text-lg focus:outline-none focus:border-gray-400 focus:ring-2 focus:ring-gray-200 transition-all payment-input"
                  placeholder="0.00"
                  :disabled="remainingBalance <= 0"
                >
                <div class="pt-2">
                  <button 
                    @click="setFullPaymentAmount"
                    class="w-full px-5 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-400 rounded-lg hover:bg-gray-50 transition-colors flex justify-center items-center"
                    title="Completar con el monto faltante"
                  >
                    Pagar todo
                    <span class="hidden sm:inline ml-1">
                      ({{ formatCurrency(remainingBalance) }})
                    </span>
                  </button>
                </div>
                
                <!-- Estado del pago actual -->
                <div v-if="getCurrentAmount > 0" class="mt-6 p-6 rounded-lg text-center" :class="getStatusClass">
                  <div v-if="getCurrentAmount < remainingBalance">
                    <p class="text-xs text-gray-500">Falta por pagar</p>
                    <p class="text-lg sm:text-xl font-bold text-red-600">{{ formatCurrency(remainingBalance - getCurrentAmount) }}</p>
                  </div>
                  <div v-else-if="getCurrentAmount === remainingBalance">
                    <p class="text-xs text-green-600">Pago exacto</p>
                  </div>
                  <div v-else-if="selectedPaymentMethod === PAYMENT_CODES.CASH">
                    <p class="text-xs text-gray-500">Vuelto</p>
                    <p class="text-lg sm:text-xl font-bold text-green-600">{{ formatCurrency(getCurrentAmount - remainingBalance) }}</p>
                  </div>
                </div>
              </div>

              <!-- Botón de registrar pago -->
              <button 
                v-if="selectedPaymentMethod && remainingBalance > 0 && getCurrentAmount > 0"
                @click="addPayment"
                class="w-full py-2 bg-gray-800 text-white rounded-lg font-semibold hover:bg-gray-800 transition-all text-sm sm:text-base"
              >
                Registrar pago
              </button>

              <!-- Pagos registrados -->
              <div v-if="payments.length > 0" class="border-t border-gray-200 pt-3">
                <p class="text-xs font-semibold text-gray-500 mb-2">Pagos realizados</p>
                <div class="space-y-1 max-h-[150px] overflow-y-auto">
                  <div v-for="(payment, idx) in payments" :key="idx" class="flex justify-between items-center text-xs sm:text-sm p-2 bg-gray-50 rounded-lg border border-gray-300">
                    <div class="flex gap-2">
                      <span class="font-semibold">{{ payment.method === PAYMENT_CODES.YAPE ? 'Yape' : 'Efectivo' }}</span>
                    </div>
                    <div class="flex items-center gap-4">
                      <span class="font-bold">{{ formatCurrency(payment.received || payment.amount) }}</span>
                      <button @click="removePayment(idx)" class="text-red-400 hover:text-red-500 text-sm text-bold">×</button>
                    </div>
                  </div>
                </div>
                <p class="text-xs text-gray-600 mt-2 text-right">Total pagado: {{ formatCurrency(totalPaid) }}</p>
              </div>
            </div>
          </div>
          
          <!-- Totales y botón finalizar - Fijo al final -->
          <div class="border-t border-gray-200 p-4 sm:p-5 bg-gray-50 flex-shrink-0">
            <div class="space-y-1 mb-4">
              <div class="flex justify-between text-xs sm:text-sm">
                <span class="text-gray-600">Subtotal</span>
                <span class="text-gray-800 font-medium">{{ formatCurrency(subtotal) }}</span>
              </div>
              <div class="flex justify-between text-xs sm:text-sm">
                <span class="text-gray-600">IGV (0%)</span>
                <span class="text-gray-800 font-medium">{{ formatCurrency(igvTotal) }}</span>
              </div>
              <div class="flex justify-between pt-2 border-t border-gray-200">
                <span class="text-base sm:text-lg font-bold text-gray-900">Total</span>
                <span class="text-base sm:text-lg font-bold text-gray-900">{{ formatCurrency(total) }}</span>
              </div>
              <div v-if="remainingBalance > 0" class="flex justify-between pt-1">
                <span class="text-sm text-red-600">Saldo pendiente</span>
                <span class="text-sm font-bold text-red-600">{{ formatCurrency(remainingBalance) }}</span>
              </div>
            </div>  
            <button 
              @click="finalizeSale"
              :disabled="remainingBalance > 0 || cart.length === 0 || procesandoVenta"
              :class="remainingBalance > 0
                ? 'bg-red-300 hover:bg-red-400'
                : 'bg-green-600 hover:bg-green-700'"
              class="w-full py-2.5 sm:py-3 text-white text-sm sm:text-base font-semibold rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
            >
              {{ procesandoVenta ? 'Procesando...' : (remainingBalance > 0 ? `Faltan ${formatCurrency(remainingBalance)}` : 'Finalizar venta') }}
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- MODAL DE BÚSQUEDA DE PRODUCTOS CON PAGINADOR -->
    <div v-if="showProductModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full h-auto max-h-[80vh] flex flex-col animate-fadeInUp">
        
        <div class="px-5 sm:px-6 py-3 sm:py-4 border-b border-gray-200 flex justify-between items-center bg-white rounded-t-2xl">
          <div>
            <h3 class="text-base sm:text-lg font-semibold text-gray-900">Buscar productos</h3>
            <p class="text-xs text-gray-500 mt-0.5">Seleccione los productos para agregar al carrito</p>
          </div>
          <button @click="closeProductModal" class="text-gray-400 hover:text-gray-600 text-2xl leading-none w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100">
            ×
          </button>
        </div>
        
        <div class="p-4 sm:p-5 border-b border-gray-200 bg-gray-50">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input 
              ref="modalSearchInput"
              v-model="modalSearchTerm"
              @input="handleModalSearch"
              type="text"
              placeholder="Buscar por nombre o código de barras..."
              class="w-full pl-9 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-gray-400 focus:ring-2 focus:ring-gray-200 transition-all"
              autofocus
            />
          </div>
        </div>
        
        <div class="flex-1 overflow-auto p-4 sm:p-5">
          <div v-if="modalLoading" class="text-center py-16">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-2 border-gray-300 border-t-gray-600"></div>
            <p class="mt-3 text-sm text-gray-500">Buscando productos...</p>
          </div>
          
          <div v-else-if="modalProducts.length === 0" class="text-center py-16">
            <svg class="w-16 h-16 text-gray-300 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
            </svg>
            <p class="text-gray-400 text-sm">No se encontraron productos</p>
          </div>
          
          <div v-else>
            <div class="overflow-x-auto">
              <table class="min-w-full text-sm">
                <thead class="bg-gray-50 sticky top-0">
                  <tr>
                    <th class="px-2 py-1.5 text-left text-xs font-medium text-gray-500">Código Barra</th>
                    <th class="px-2 py-1.5 text-left text-xs font-medium text-gray-500">Producto</th>
                    <th class="px-2 py-1.5 text-right text-xs font-medium text-gray-500">Precio</th>
                    <th class="px-2 py-1.5 text-center text-xs font-medium text-gray-500">Stock</th>
                    <th class="px-2 py-1.5 text-center text-xs font-medium text-gray-500">Estado</th>
                    <th class="px-2 py-1.5 text-center text-xs font-medium text-gray-500">Acción</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr 
                    v-for="product in modalProducts" 
                    :key="product.id"
                    @dblclick="agregarDesdeModal(product)"
                    class="hover:bg-gray-50 cursor-pointer transition-colors text-sm"
                  >
                    <td class="px-2 py-1.5 text-xs text-gray-500">{{ product.codigo_barra || 'Sin código' }}</td>
                    <td class="px-2 py-1.5 text-sm text-gray-800">{{ product.nombre_producto }}</td>
                    <td class="px-2 py-1.5 text-right text-sm font-bold text-gray-900">{{ formatCurrency(product.precio_unitario) }}</td>
                    <td class="px-2 py-1.5 text-center">
                      <span :class="[
                        'text-xs px-1.5 py-0.5 rounded-full',
                        product.cantidad_producto <= 5 ? 'bg-yellow-100 text-yellow-700' : 'bg-gray-100 text-gray-600'
                      ]">
                        {{ product.cantidad_producto }}
                      </span>
                    </td>
                    <td class="px-2 py-1.5 text-center">
                      <span :class="product.estado ? 'bg-green-50 text-green-700' : 'bg-red-100 text-red-600'"
                        class="inline-block px-2 py-0.5 rounded-full text-xs font-medium">
                        {{ product.estado ? "Activo" : "Inactivo" }}
                      </span>
                    </td>
                    <td class="px-2 py-1.5 text-center">
                      <button 
                        @click.stop="agregarDesdeModal(product)"
                        :disabled="product.estado === false || product.estado === 'false' || product.cantidad_producto <= 0"
                        class="px-2 py-1 text-xs bg-gray-800 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 transition-colors"
                      >
                        Agregar
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- PAGINADOR DEL MODAL -->
            <div v-if="modalPagination && modalPagination.total > 0 && !modalLoading" 
                 class="mt-4 pt-4 border-t border-gray-200">
              <div class="flex items-center justify-between flex-wrap gap-2">
                <div class="text-xs text-gray-500">
                  Mostrando {{ ((modalPagination.currentPage - 1) * modalPageSize) + 1 }} - 
                  {{ Math.min(modalPagination.currentPage * modalPageSize, modalPagination.total) }} 
                  de {{ modalPagination.total }} productos
                </div>
                <div class="flex gap-2">
                  <button 
                    @click="cambiarPaginaModal(modalPagination.currentPage - 1)"
                    :disabled="modalPagination.currentPage === 1"
                    class="px-3 py-1.5 text-xs border border-gray-200 rounded-lg hover:bg-white hover:border-gray-300 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                    Anterior
                  </button>
                  
                  <span class="px-3 py-1.5 text-xs text-gray-600">
                    Página {{ modalPagination.currentPage }} de {{ modalPagination.totalPages }}
                  </span>
                  
                  <button 
                    @click="cambiarPaginaModal(modalPagination.currentPage + 1)"
                    :disabled="modalPagination.currentPage === modalPagination.totalPages"
                    class="px-3 py-1.5 text-xs border border-gray-200 rounded-lg hover:bg-white hover:border-gray-300 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
                  >
                    Siguiente
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="px-5 sm:px-6 py-3 sm:py-4 border-t border-gray-200 bg-gray-50 flex justify-between items-center rounded-b-2xl">
          <p class="text-xs text-gray-500">Doble click en la fila o presione "Agregar"</p>
          <button @click="closeProductModal" class="px-4 py-1.5 bg-gray-800 text-white text-sm rounded-lg hover:bg-gray-700 transition-colors">
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { list_producto } from '../../productos/api/producto.ts';
import { create_venta, producto_list_x_codigo } from '../api/venta';
import {
  PAYMENT_CODES,
  formatCurrency,
  roundToTwoDecimals,
  sanitizeCurrencyInput,
  parseCurrencyInput,
  calculateTotals,
  updatePaymentCalculations,
  createYapePayment,
  showToast,
  showErrorAlert,
  showSaleCompletedAlert,
  showPaymentCompletedAlert,
  showProductInactiveAlert,
  showInsufficientStockAlert,
  showNoStockAlert,
  showEmptyCartAlert,
  showInvalidAmountAlert,
  showIncompletePaymentAlert,
  showSaleErrorAlert,
  getCurrentDateFormatted,
  playBeep
} from '../utils/utils.ts';

export default {
  name: "POSVentas",
  data() {
    return {
      PAYMENT_CODES,
      
      // Carrito
      cart: [],
      
      // Modal de búsqueda
      showProductModal: false,
      modalSearchTerm: "",
      modalProducts: [],
      modalLoading: false,
      modalSearchTimeout: null,
      modalPagination: null,
      modalCurrentPage: 1,
      modalPageSize: 10,
      
      // Pago
      selectedPaymentMethod: null,
      payments: [],
      cashAmount: null,
      cashAmountText: '',
      yapeAmount: null,
      yapeAmountText: '',
      procesandoVenta: false,
      isPaymentInputFocused: false,
      totals: {
        subtotal: 0,
        igvTotal: 0,
        total: 0,
        totalPaid: 0,
        remainingBalance: 0,
        totalVuelto: 0
      },
      
      // ESCÁNER: Variables para el código de barras
      codigoEscaneado: '',
      escaneoTimeout: null,
      lastKeyTime: null,
      escaneando: false 
    };
  },
  computed: {
    currentDate() {
      return getCurrentDateFormatted();
    },
    nombreUsuario() {
      try {
        const auth = localStorage.getItem("auth");
        if (auth) {
          const data = JSON.parse(auth);
          return data.user?.nombre || 'Administrador';
        }
        return 'Administrador';
      } catch (error) {
        return 'Administrador';
      }
    },
    subtotal() { return this.totals.subtotal; },
    igvTotal() { return this.totals.igvTotal; },
    total() { return this.totals.total; },
    totalPaid() { return this.totals.totalPaid; },
    remainingBalance() { return this.totals.remainingBalance; },
    totalVuelto() { return this.totals.totalVuelto; },
    totalRecibido() {
      return this.payments.reduce((sum, p) => sum + (p.received || p.amount), 0);
    },
    getCurrentAmount() {
      if (this.selectedPaymentMethod === PAYMENT_CODES.CASH) return this.cashAmount || 0;
      if (this.selectedPaymentMethod === PAYMENT_CODES.YAPE) return this.yapeAmount || 0;
      return 0;
    },
    getStatusClass() {
      const amount = this.getCurrentAmount;
      if (!amount || amount <= 0) return '';
      if (amount < this.remainingBalance) return 'bg-red-50 border border-red-200';
      if (amount === this.remainingBalance) return 'bg-green-50 border border-green-200';
      if (this.selectedPaymentMethod === PAYMENT_CODES.CASH) return 'bg-green-50 border border-green-200';
      return 'bg-red-50 border border-red-200';
    },
    idUsuarioVenta() {
      try {
        const auth = localStorage.getItem("auth");
        if (auth) {
          const data = JSON.parse(auth);
          return data.user?.id || 1;
        }
        return 1;
      } catch (error) {
        return 1;
      }
    }
  },
  watch: {
    cart: { deep: true, handler() { this.updateTotals(); } },
    payments: { deep: true, handler() { this.updateTotals(); } }
  },
  mounted() {
    this.updateTotals();
  },
  beforeDestroy() {
    if (this.modalSearchTimeout) {
      clearTimeout(this.modalSearchTimeout);
      this.modalSearchTimeout = null;
    }
    if (this.escaneoTimeout) {
      clearTimeout(this.escaneoTimeout);
      this.escaneoTimeout = null;
    }
    this.escaneando = false;
  },
  methods: {
    formatCurrency,

    isProductActive(product) {
      return product.estado === true || product.estado === 'true' || product.estado === 1;
    },

    // ==================== MÉTODOS PARA CONTROLAR EL FOCO DEL INPUT DE PAGO ====================
    onPaymentInputFocus() {
      this.isPaymentInputFocused = true;
      console.log('💰 Input de pago enfocado - escáner desactivado');
    },
    
    onPaymentInputBlur() {
      this.isPaymentInputFocused = false;
      console.log('💰 Input de pago perdió foco - escáner reactivado');
    },

    // ==================== ESCÁNER DE CÓDIGO DE BARRAS ====================
    // ✅ ELIMINÉ iniciarListenerEscanner y detenerListenerEscanner
    
    handlePaste(event) {
      const target = event.target;
      
      // Si el modal está abierto, solo llenar el input de búsqueda
      if (this.showProductModal) {
        console.log('📋 Modal abierto - pegando código en búsqueda');
        event.preventDefault();
        const pastedText = event.clipboardData?.getData('text') || '';
        if (pastedText) {
          this.modalSearchTerm = pastedText.trim();
          this.handleModalSearch();
        }
        return;
      }
      
      // Verificar si estamos en un input de pago
      const isPaymentInput = target.tagName === 'INPUT' && 
        (target.classList.contains('payment-input') ||
        target.placeholder?.toLowerCase().includes('monto') ||
        target.placeholder?.toLowerCase().includes('recibido'));
      
      if (isPaymentInput) {
        console.log('💰 Input de pago detectado, permitiendo pegado normal');
        return;
      }
      
      const pastedText = event.clipboardData?.getData('text') || '';
      
      if (pastedText) {
        console.log('📋 Texto pegado:', pastedText);
        event.preventDefault();
        const codigo = pastedText.trim();
        if (codigo) {
          this.buscarProductoPorCodigo(codigo);
        }
      }
    },
    
    handleKeydown(event) {
      const target = event.target;
      
      if (this.showProductModal) {
        const isModalSearchInput = this.$refs.modalSearchInput && target === this.$refs.modalSearchInput;
        if (isModalSearchInput) {
          return;
        }
        console.log('Modal abierto, ignorando escáner');
        return;
      }
      if (this.isPaymentInputFocused) {
        console.log('Input de pago enfocado, ignorando teclas');
        return;
      }
    
      const isPaymentInput = target.tagName === 'INPUT' && 
        (target.classList.contains('payment-input') ||
        target.placeholder?.toLowerCase().includes('monto') ||
        target.placeholder?.toLowerCase().includes('recibido'));
      
      if (isPaymentInput) {
        console.log('Input de pago detectado, ignorando escáner');
        return;
      }
      
      if (event.ctrlKey && event.key === 'v') {
        return;
      }
      
      const now = Date.now();
      if (this.lastKeyTime && (now - this.lastKeyTime) > 100) {
        this.codigoEscaneado = '';
      }
      this.lastKeyTime = now;
      
      if (event.key.length === 1 && !event.ctrlKey && !event.altKey && !event.metaKey) {
        this.codigoEscaneado += event.key;
        
        if (this.escaneoTimeout) clearTimeout(this.escaneoTimeout);
        
        this.escaneoTimeout = setTimeout(() => {
          if (this.codigoEscaneado.trim()) {
            this.procesarEscaneo();
          }
        }, 50);
      }
      
      if (event.key === 'Enter' && this.codigoEscaneado.trim()) {
        event.preventDefault();
        this.procesarEscaneo();
      }
    },
    
    async procesarEscaneo() {
      // ✅ Si ya hay un escaneo en proceso, ignorar
      if (this.escaneando) {
        console.log('Escaneo en proceso, ignorando...');
        return;
      }
      
      const codigo = this.codigoEscaneado.trim();
      
      if (!codigo) {
        this.codigoEscaneado = '';
        return;
      }

      this.escaneando = true;
      console.log('Escaneando código:', codigo);
      const codigoProcesar = codigo;
      this.codigoEscaneado = '';
      
      try {
        await this.buscarProductoPorCodigo(codigoProcesar);
      } catch (error) {
        console.error('Error en escaneo:', error);
      } finally {
        this.escaneando = false;
      }
    },
    
    async buscarProductoPorCodigo(codigoBarra) {
      console.log('Buscando producto con código:', codigoBarra);
      
      if (!codigoBarra || codigoBarra.trim() === '') {
        console.log('Código vacío');
        return false;
      }
      
      try {
        const response = await producto_list_x_codigo(codigoBarra, 'true');
        
        const producto = response.data;
        
        if (!producto || !producto.id) {
          console.log('Producto no encontrado:', codigoBarra);
          showErrorAlert(`Producto no encontrado: ${codigoBarra}`);
          playBeep();
          return false;
        }
        
        console.log('Producto encontrado:', producto.nombre_producto);
        
        if (!this.isProductActive(producto)) {
          showProductInactiveAlert(producto.nombre_producto);
          playBeep();
          return false;
        }
        
        if (producto.cantidad_producto <= 0) {
          showNoStockAlert(producto.nombre_producto);
          playBeep();
          return false;
        }
        
        const existingItem = this.cart.find(item => item.id === producto.id);
        
        if (existingItem) {
          if (existingItem.quantity < producto.cantidad_producto) {
            existingItem.quantity++;
            showToast(`"${producto.nombre_producto}" cantidad aumentada a ${existingItem.quantity}`, 'success');
            playBeep();
          } else {
            showInsufficientStockAlert(producto.nombre_producto, producto.cantidad_producto);
            playBeep();
          }
        } else {
          this.agregarProductoAlCarrito(producto);
          showToast(`"${producto.nombre_producto}" agregado al carrito`, 'success');
          playBeep();
        }
        
        return true;
        
      } catch (error) {        
        if (error.response && error.response.status === 404) {
          showErrorAlert(`Producto no encontrado: ${codigoBarra}`);
        } else {
          console.error('Error en búsqueda:', error);
          showErrorAlert('Error al buscar el producto');
        }
        playBeep();
        return false;
      }
    },

    agregarProductoAlCarrito(producto) {
      console.log('Agregando al carrito:', producto.nombre_producto);
      const existing = this.cart.find(item => item.id === producto.id);
      
      if (existing) {
        if (existing.quantity < producto.cantidad_producto) {
          existing.quantity++;
          console.log('Cantidad actualizada:', existing.quantity);
        } else {
          showInsufficientStockAlert(producto.nombre_producto, producto.cantidad_producto);
        }
      } else {
        this.cart.push({ ...producto, quantity: 1 });
        console.log('Producto nuevo agregado, carrito tiene:', this.cart.length, 'productos');
      }
    },

    setFullPaymentAmount() {
      if (this.selectedPaymentMethod === PAYMENT_CODES.CASH) {
        const amount = this.remainingBalance;
        this.cashAmount = amount;
        this.cashAmountText = amount.toFixed(2);
      } else if (this.selectedPaymentMethod === PAYMENT_CODES.YAPE) {
        const amount = this.remainingBalance;
        this.yapeAmount = amount;
        this.yapeAmountText = amount.toFixed(2);
      }
    },
    
    // ==================== CARRITO ====================
    updateQuantity(index, delta) {
      const item = this.cart[index];
      const newQty = item.quantity + delta;
      if (newQty <= 0) {
        this.cart.splice(index, 1);
      } else if (newQty <= item.cantidad_producto) {
        item.quantity = newQty;
      } else {
        showInsufficientStockAlert(item.nombre_producto, item.cantidad_producto);
      }
    },
    
    removeFromCart(index) {
      this.cart.splice(index, 1);
    },
    
    updateTotals() {
      const baseTotals = calculateTotals(this.cart);
      this.totals = updatePaymentCalculations(baseTotals, this.payments);
    },
    
    // ==================== PAGO ====================
    togglePaymentMethod(method) {
      if (this.selectedPaymentMethod === method) {
        this.selectedPaymentMethod = null;
        this.cashAmount = null;
        this.cashAmountText = '';
        this.yapeAmount = null;
        this.yapeAmountText = '';
      } else {
        this.selectedPaymentMethod = method;
        if (method === PAYMENT_CODES.YAPE && this.remainingBalance > 0) {
          this.$nextTick(() => {
            this.registrarPagoYapeAutomatico();
          });
        }
      }
    },

    registrarPagoYapeAutomatico() {
      if (this.selectedPaymentMethod === PAYMENT_CODES.YAPE && this.remainingBalance > 0) {
        const amount = this.remainingBalance;
        this.yapeAmount = amount;
        this.yapeAmountText = amount.toString();
        this.addPaymentYape();
        showToast(`Pago Yape automático de ${formatCurrency(amount)} registrado`, 'success');
      }
    },
    
    updateYapeAmount(event) {
      try {
        const value = event.target.value;
        const sanitized = sanitizeCurrencyInput(value);
        this.yapeAmountText = sanitized;
        let amount = parseCurrencyInput(sanitized);
        if (isNaN(amount)) amount = 0;
        if (amount > this.remainingBalance) {
          amount = this.remainingBalance;
          this.yapeAmountText = amount.toFixed(2);
        }
        this.yapeAmount = amount;
      } catch (error) {
        console.error('Error actualizando monto Yape:', error);
        this.yapeAmount = 0;
        this.yapeAmountText = '0';
      }
    },
    
    updateCashAmount(event) {
      try {
        const value = event.target.value;
        const sanitized = sanitizeCurrencyInput(value);
        this.cashAmountText = sanitized;
        let amount = parseCurrencyInput(sanitized);
        if (isNaN(amount)) amount = 0;
        this.cashAmount = amount;
      } catch (error) {
        console.error('Error actualizando monto efectivo:', error);
        this.cashAmount = 0;
        this.cashAmountText = '0';
      }
    },
    
    addPayment() {
      if (!this.selectedPaymentMethod) {
        showErrorAlert('Seleccione un método de pago');
        return;
      }
      if (this.selectedPaymentMethod === PAYMENT_CODES.CASH) {
        this.addPaymentEfectivo();
      } else if (this.selectedPaymentMethod === PAYMENT_CODES.YAPE) {
        this.addPaymentYape();
      }
    },
    
    addPaymentYape() {
      let amount = this.yapeAmount;
      if (!amount || amount <= 0) {
        showErrorAlert('Ingrese un monto válido');
        return;
      }
      if (amount > this.remainingBalance) {
        showErrorAlert(`El monto no puede exceder el saldo pendiente (${formatCurrency(this.remainingBalance)})`);
        return;
      }
      amount = roundToTwoDecimals(amount) || 0;
      const payment = createYapePayment(amount);
      this.payments.push(payment);
      this.yapeAmount = null;
      this.yapeAmountText = '';
      this.selectedPaymentMethod = null;
      if (this.remainingBalance <= 0) {
        showPaymentCompletedAlert(this.totalPaid, this.totalVuelto);
      }
    },
    
    addPaymentEfectivo() {
      let amount = this.cashAmount;
      if (!amount || amount <= 0) {
        showInvalidAmountAlert();
        return;
      }
      amount = roundToTwoDecimals(amount) || 0;
      let paymentAmount = amount;
      let changeAmount = 0;
      if (amount >= this.remainingBalance) {
        paymentAmount = this.remainingBalance;
        changeAmount = roundToTwoDecimals(amount - this.remainingBalance) || 0;
      }
      const payment = {
        method: PAYMENT_CODES.CASH,
        amount: paymentAmount,
        changeAmount: changeAmount,
        received: amount,
        date: new Date().toLocaleTimeString()
      };
      this.payments.push(payment);
      this.cashAmount = null;
      this.cashAmountText = '';
      this.selectedPaymentMethod = null;
      if (this.remainingBalance <= 0) {
        showPaymentCompletedAlert(this.totalPaid, this.totalVuelto);
      }
    },
    
    removePayment(index) {
      if (confirm('¿Estás seguro de eliminar este pago?')) {
        this.payments.splice(index, 1);
        showToast('Pago eliminado', 'info');
      }
    },
    
    // ==================== MODAL DE BÚSQUEDA ====================
    openProductModal() {
      this.showProductModal = true;
      this.modalSearchTerm = "";
      this.modalProducts = [];
      this.modalPagination = null;
      this.modalCurrentPage = 1;
      this.cargarProductosModal(1);
      this.$nextTick(() => {
        if (this.$refs.modalSearchInput) {
          this.$refs.modalSearchInput.focus();
        }
      });
      console.log('Modal abierto');
    },
    
    closeProductModal() {
      this.showProductModal = false;
      this.modalSearchTerm = "";
      this.modalProducts = [];
      this.modalPagination = null;
      if (this.modalSearchTimeout) clearTimeout(this.modalSearchTimeout);
      console.log('Modal cerrado');
    },
    
    handleModalSearch() {
      if (this.modalSearchTimeout) clearTimeout(this.modalSearchTimeout);
      this.modalSearchTimeout = setTimeout(() => {
        this.cargarProductosModal(1);
      }, 400);
    },
    
    async cargarProductosModal(page = 1) {
      this.modalLoading = true;
      this.modalCurrentPage = page;
      
      try {
        const params = { 
          page: page, 
          page_size: this.modalPageSize 
        };
        
        if (this.modalSearchTerm) {
          params.search = this.modalSearchTerm;
        }
        
        const response = await list_producto(params);
        
        if (response.data && response.data.results) {
          this.modalProducts = response.data.results;
          
          this.modalPagination = {
            count: response.data.count || 0,
            next: response.data.next,
            previous: response.data.previous,
            total: response.data.count || 0,
            currentPage: page,
            totalPages: Math.ceil((response.data.count || 0) / this.modalPageSize)
          };
        } else {
          this.modalProducts = [];
          this.modalPagination = null;
        }
      } catch (error) {
        console.error("Error buscando productos:", error);
        this.modalProducts = [];
        this.modalPagination = null;
      } finally {
        this.modalLoading = false;
      }
    },
    
    cambiarPaginaModal(page) {
      if (page >= 1 && page <= this.modalPagination?.totalPages) {
        this.cargarProductosModal(page);
      }
    },
    
    agregarDesdeModal(product) {
      if (!this.isProductActive(product)) {  // ✅ Usar el helper
        showProductInactiveAlert(product.nombre_producto);
        return;
      }
      
      if (product.cantidad_producto <= 0) {
        showNoStockAlert(product.nombre_producto);
        return;
      }
      
      const existing = this.cart.find(item => item.id === product.id);
      if (existing) {
        if (existing.quantity < product.cantidad_producto) {
          existing.quantity++;
          showToast(`Cantidad aumentada: ${product.nombre_producto}`, 'success');
        } else {
          showInsufficientStockAlert(product.nombre_producto, product.cantidad_producto);
        }
      } else {
        this.cart.push({ ...product, quantity: 1 });
        showToast(`"${product.nombre_producto}" agregado al carrito`, 'success');
      }
      
      playBeep();
    },
    
    // ==================== FINALIZAR VENTA ====================
    async finalizeSale() {

      if (this.cart.length === 0) {
        showEmptyCartAlert();
        return;
      }

      if (this.showProductModal) {
        this.closeProductModal();
      }
      
      if (this.remainingBalance > 0) {
        showIncompletePaymentAlert(this.remainingBalance);
        return;
      }
      
      if (this.procesandoVenta) return;
      this.procesandoVenta = true;
      
      try {
        const detalles = this.cart.map(item => ({
          descripcion_producto: item.nombre_producto,
          codigo_barra: item.codigo_barra || '',
          codigo_interno: item.codigo_interno || '',
          cantidad_venta: item.quantity,
          producto_id: item.id,
          precio_venta: parseFloat(item.precio_unitario),
          sub_total_venta: parseFloat((item.precio_unitario * item.quantity).toFixed(2))
        }));

        const pagos = this.payments.map(payment => {
          const pago = { forma_pago: payment.method, monto_pagar: payment.amount };
          if (payment.method === PAYMENT_CODES.CASH) {
            pago.efectivo_recibido = payment.received || payment.amount;
            pago.efectivo_vuelto = payment.changeAmount || 0;
          }
          return pago;
        });
        
        const response = await create_venta({
          id_usuario_venta: this.idUsuarioVenta,
          detalles: detalles,
          pagos: pagos
        });
        
        if (response.data.success) {
          await showSaleCompletedAlert(response.data.correlativo, this.total);
          this.cart = [];
          this.payments = [];
          this.selectedPaymentMethod = null;
          this.cashAmount = null;
          this.cashAmountText = '';
          this.yapeAmount = null;
          this.yapeAmountText = '';
        } else {
          showSaleErrorAlert('Error al registrar la venta');
        }
      } catch (error) {
        console.error('Error al registrar venta:', error);
        showSaleErrorAlert('Error al registrar la venta');
      } finally {
        this.procesandoVenta = false;
      }
    }
  }
};
</script>

<style scoped>
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeInUp {
  animation: fadeInUp 0.3s ease-out;
}
</style>