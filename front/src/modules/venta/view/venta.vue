<template>
  <div class="h-full min-h-0 overflow-hidden bg-gray-100 flex flex-col">
    <!-- Contenido principal -->
    <main class="h-full min-h-0 overflow-y-auto lg:overflow-hidden p-4 sm:p-6">
      <div class="w-full min-h-0 lg:h-full grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-[1600px] mx-auto">

        <!-- Carrito -->
        <section class="lg:col-span-2 min-h-[420px] lg:min-h-0 flex flex-col bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
          
          <!-- Header del carrito -->
          <div class="px-6 py-4 border-b border-gray-200 bg-gray-50 flex-shrink-0">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
              <div class="flex items-center gap-3">
                <div class="w-1 h-6 bg-gray-800 rounded-full"></div>
                <div>
                  <h2 class="text-sm font-bold text-gray-800">Carrito</h2>
                  <p class="text-xs text-gray-500">Productos agregados</p>
                </div>
              </div>

              <div class="flex items-center gap-3">
                <span class="text-xs font-semibold text-gray-700 bg-gray-200 px-3 py-1.5 rounded-lg">
                  {{ cart.length }} {{ cart.length === 1 ? "producto" : "productos" }}
                </span>

                <button @click="openProductModal" class="px-4 py-2 text-xs font-semibold text-white bg-gray-800 rounded-lg hover:bg-gray-900 transition-colors duration-200 shadow-sm hover:shadow">
                  Buscar producto
                </button>
              </div>
            </div>
          </div>

          <!-- Área del carrito -->
          <div class="flex-1 min-h-0 overflow-auto">
            <div v-if="cart.length === 0" class="h-full min-h-[330px] flex flex-col items-center justify-center text-center p-8">
              <div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mb-4">
                <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
              </div>
              <p class="text-sm font-semibold text-gray-600">Carrito vacío</p>
              <p class="text-xs text-gray-400 mt-1">Agregue productos para continuar</p>
            </div>

            <div v-else class="h-full overflow-auto">
              <table class="min-w-[920px] w-full text-sm">
                <thead class="bg-gray-100 sticky top-0 z-10 border-b border-gray-200">
                  <tr>
                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Código</th>
                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Producto</th>
                    <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">Stock</th>
                    <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">Cantidad</th>
                    <th class="px-4 py-3 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">Precio</th>
                    <th class="px-4 py-3 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">Subtotal</th>
                    <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider"></th>
                  </tr>
                </thead>

                <tbody class="divide-y divide-gray-100">
                  <tr v-for="(item, index) in cart" :key="item.id" class="hover:bg-gray-50 transition-colors duration-150">
                    <td class="px-4 py-3.5 text-xs text-gray-600 whitespace-nowrap font-medium">
                      {{ item.codigo_barra || "—" }}
                    </td>

                    <td class="px-4 py-3.5">
                      <p class="max-w-[360px] truncate text-sm font-semibold text-gray-800">
                        {{ item.nombre_producto }}
                      </p>
                    </td>

                    <td class="px-4 py-3.5 text-center">
                      <span :class="[
                        'text-xs font-semibold px-2.5 py-0.5 rounded-full',
                        item.cantidad_producto <= 5 ? 'bg-red-100 text-red-700' : 
                        item.cantidad_producto <= 10 ? 'bg-amber-100 text-amber-700' : 
                        'bg-emerald-100 text-emerald-700'
                      ]">
                        {{ item.cantidad_producto }}
                      </span>
                    </td>

                    <td class="px-4 py-3.5">
                      <div class="flex items-center justify-center gap-2">
                        <button @click="updateQuantity(index, -1)" class="w-7 h-7 rounded-lg border border-gray-300 bg-white text-gray-600 hover:bg-gray-100 hover:border-gray-400 transition-colors duration-200 text-sm flex items-center justify-center font-bold">
                          −
                        </button>
                        <span class="text-sm font-bold text-gray-800 w-8 text-center">
                          {{ item.quantity }}
                        </span>
                        <button @click="updateQuantity(index, 1)" class="w-7 h-7 rounded-lg border border-gray-300 bg-white text-gray-600 hover:bg-gray-100 hover:border-gray-400 transition-colors duration-200 text-sm flex items-center justify-center font-bold">
                          +
                        </button>
                      </div>
                    </td>

                    <td class="px-4 py-3.5 text-right text-sm font-medium text-gray-700 whitespace-nowrap">
                      {{ formatCurrency(item.precio_unitario) }}
                    </td>

                    <td class="px-4 py-3.5 text-right font-bold text-gray-800 whitespace-nowrap">
                      {{ formatCurrency(item.precio_unitario * item.quantity) }}
                    </td>

                    <td class="px-4 py-3.5 text-center">
                      <button @click="removeFromCart(index)" class="text-red-500 hover:text-red-700 transition-colors duration-200 text-xl leading-none font-bold hover:scale-110 transform">
                        ×
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- Pago -->
        <section class="lg:col-span-1 min-h-[420px] lg:min-h-0 flex flex-col bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
          
          <!-- Header -->
          <div class="px-6 py-4 border-b border-gray-200 bg-gray-50 flex-shrink-0">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-1 h-6 bg-gray-800 rounded-full"></div>
                <div>
                  <h2 class="text-sm font-bold text-gray-800">Pago</h2>
                  <p class="text-xs text-gray-500">Registre los pagos</p>
                </div>
              </div>

              <div v-if="remainingBalance > 0" class="text-right">
                <p class="text-[10px] font-semibold text-gray-500 uppercase tracking-wider">Pendiente</p>
                <p class="text-sm font-bold text-amber-600">{{ formatCurrency(remainingBalance) }}</p>
              </div>
            </div>
          </div>

          <!-- Contenido -->
          <div class="flex-1 min-h-0 overflow-y-auto">
            <div class="p-5 space-y-5">

              <!-- Métodos de pago -->
              <div>
                <p class="text-xs font-semibold text-gray-600 mb-2.5">Método de pago</p>
                <div class="grid grid-cols-2 gap-2">
                  <button @click="togglePaymentMethod(PAYMENT_CODES.CASH)" :class="[
                    'py-2.5 px-3 rounded-lg border-2 text-sm font-semibold transition-colors duration-200',
                    selectedPaymentMethod === PAYMENT_CODES.CASH
                      ? 'border-green-600 bg-green-600 text-white shadow-sm'
                      : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
                  ]">
                    Efectivo
                  </button>
                  <button @click="togglePaymentMethod(PAYMENT_CODES.YAPE)" :class="[
                    'py-2.5 px-3 rounded-lg border-2 text-sm font-semibold transition-colors duration-200',
                    selectedPaymentMethod === PAYMENT_CODES.YAPE
                      ? 'border-purple-600 bg-purple-600 text-white shadow-sm'
                      : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
                  ]">
                    Yape
                  </button>
                </div>
              </div>

              <!-- Área de pago -->
              <div v-if="selectedPaymentMethod && remainingBalance > 0" class="space-y-3">
                <div>
                  <label class="block text-xs font-semibold text-gray-600 mb-1.5">
                    {{ selectedPaymentMethod === PAYMENT_CODES.CASH ? "Monto recibido" : "Monto a pagar" }}
                  </label>
                  <div class="relative">
                    <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-500 font-bold text-base">S/</span>
                    <input ref="cashInput"
                      :value="selectedPaymentMethod === PAYMENT_CODES.CASH ? cashAmountText : yapeAmountText"
                      @input="selectedPaymentMethod === PAYMENT_CODES.CASH ? updateCashAmount($event) : updateYapeAmount($event)"
                      @focus="onPaymentInputFocus" @blur="onPaymentInputBlur" type="number" inputmode="decimal"
                      class="w-full pl-9 pr-3.5 py-2.5 border-2 border-gray-300 rounded-lg text-base font-bold focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-200 transition-all duration-200 bg-white"
                      placeholder="0.00" :disabled="remainingBalance <= 0" />
                  </div>
                </div>

                <button @click="setFullPaymentAmount" class="w-full px-3 py-2.5 text-xs font-semibold text-gray-700 border-2 border-gray-300 rounded-lg hover:bg-gray-100 hover:border-gray-400 transition-colors duration-200">
                  Pagar todo ({{ formatCurrency(remainingBalance) }})
                </button>

                <div v-if="getCurrentAmount > 0" class="py-3 px-3 rounded-lg text-center border-2" :class="getStatusClass">
                  <div v-if="getCurrentAmount < remainingBalance">
                    <p class="text-[10px] font-semibold text-gray-500 uppercase tracking-wider">Saldo pendiente</p>
                    <p class="text-base font-bold text-amber-600">{{ formatCurrency(remainingBalance - getCurrentAmount) }}</p>
                  </div>
                  <div v-else-if="getCurrentAmount === remainingBalance">
                    <p class="text-sm font-bold text-emerald-600">✓ Pago exacto</p>
                  </div>
                  <div v-else-if="selectedPaymentMethod === PAYMENT_CODES.CASH">
                    <p class="text-[10px] font-semibold text-gray-500 uppercase tracking-wider">Vuelto</p>
                    <p class="text-base font-bold text-emerald-600">{{ formatCurrency(getCurrentAmount - remainingBalance) }}</p>
                  </div>
                </div>

                <button v-if="selectedPaymentMethod && remainingBalance > 0 && getCurrentAmount > 0" @click="addPayment"
                  class="w-full py-2.5 bg-blue-600 text-white rounded-lg text-sm font-bold hover:bg-blue-700 transition-colors duration-200 shadow-sm hover:shadow">
                  Registrar pago
                </button>
              </div>

              <!-- Pagos realizados -->
              <div v-if="payments.length > 0" class="border-t-2 border-gray-200 pt-4">
                <div class="flex items-center justify-between mb-2.5">
                  <p class="text-xs font-semibold text-gray-600">Pagos realizados</p>
                </div>

                <div class="space-y-2 max-h-[120px] overflow-y-auto">
                  <div v-for="(payment, idx) in payments" :key="idx" class="flex justify-between items-center py-2.5 px-3 bg-gray-100 rounded-lg border border-gray-200">
                    <span :class="[
                      'text-sm font-semibold',
                      payment.method === PAYMENT_CODES.YAPE ? 'text-purple-700' : 'text-green-700'
                    ]">
                      {{ payment.method === PAYMENT_CODES.YAPE ? "Yape" : "Efectivo" }}
                    </span>
                    <div class="flex items-center gap-3">
                      <span class="text-sm font-bold text-gray-800">{{ formatCurrency(payment.received || payment.amount) }}</span>
                      <button @click="removePayment(idx)" class="text-red-500 hover:text-red-700 text-xl leading-none font-bold transition-colors duration-200 hover:scale-110 transform">
                        ×
                      </button>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- Totales -->
          <div class="border-t-2 border-gray-200 p-5 bg-gray-50 flex-shrink-0">
            <div class="space-y-2">
              <div class="flex justify-between text-sm">
                <span class="text-gray-500 font-medium">Subtotal</span>
                <span class="text-gray-800 font-bold">{{ formatCurrency(subtotal) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-500 font-medium">IGV (0%)</span>
                <span class="text-gray-800 font-bold">{{ formatCurrency(igvTotal) }}</span>
              </div>
              <div class="flex justify-between pt-2.5 border-t-2 border-gray-300">
                <span class="text-base font-bold text-gray-800">Total</span>
                <span class="text-base font-bold text-gray-800">{{ formatCurrency(total) }}</span>
              </div>
            </div>

            <button @click="finalizeSale" :disabled="remainingBalance > 0 || cart.length === 0 || procesandoVenta"
              class="w-full mt-4 py-3 text-sm font-bold rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow"
              :class="remainingBalance > 0
                ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
                : 'bg-emerald-600 text-white hover:bg-emerald-700'
              ">
              {{ procesandoVenta ? "Procesando..." : remainingBalance > 0 ? `Faltan ${formatCurrency(remainingBalance)}` : "Finalizar venta" }}
            </button>
          </div>
        </section>
      </div>
    </main>

    <!-- Modal de productos -->
    <div v-if="showProductModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="closeProductModal">
      <div class="bg-white rounded-xl shadow-2xl max-w-5xl w-full max-h-[90dvh] flex flex-col overflow-hidden border border-gray-200">
        
        <div class="px-6 py-4 border-b-2 border-gray-200 bg-gray-50 flex-shrink-0">
          <div class="flex justify-between items-center">
            <div>
              <h3 class="text-base font-bold text-gray-800">Buscar productos</h3>
              <p class="text-xs text-gray-500">Seleccione productos para agregar al carrito</p>
            </div>
            <button @click="closeProductModal" class="text-gray-400 hover:text-gray-600 text-2xl leading-none w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-200 transition-colors duration-200 font-light">
              ×
            </button>
          </div>
        </div>

        <div class="p-5 border-b-2 border-gray-200 flex-shrink-0">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
              <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input ref="modalSearchInput" v-model="modalSearchTerm" @input="handleModalSearch" type="text"
              placeholder="Buscar por nombre o código de barras..."
              class="w-full pl-10 pr-4 py-3 border-2 border-gray-300 rounded-lg text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all duration-200 bg-white"
              autofocus />
          </div>
        </div>

        <div class="flex-1 min-h-0 overflow-auto p-5">
          <div v-if="modalLoading" class="text-center py-20">
            <div class="inline-block animate-spin rounded-full h-10 w-10 border-4 border-blue-200 border-t-blue-600"></div>
            <p class="mt-4 text-sm font-medium text-gray-500">Cargando productos...</p>
          </div>

          <div v-else-if="modalProducts.length === 0" class="text-center py-20">
            <p class="text-base font-medium text-gray-500">No se encontraron productos</p>
          </div>

          <div v-else>
            <div class="overflow-x-auto">
              <table class="min-w-[840px] w-full text-sm">
                <thead class="bg-gray-100 sticky top-0 z-10 border-b-2 border-gray-200">
                  <tr>
                    <th class="px-4 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Código</th>
                    <th class="px-4 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Producto</th>
                    <th class="px-4 py-3.5 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">Precio</th>
                    <th class="px-4 py-3.5 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">Stock</th>
                    <th class="px-4 py-3.5 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">Estado</th>
                    <th class="px-4 py-3.5 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider"></th>
                  </tr>
                </thead>

                <tbody class="divide-y divide-gray-100">
                  <tr v-for="product in modalProducts" :key="product.id" @dblclick="agregarDesdeModal(product)" class="hover:bg-gray-50 transition-colors duration-150 cursor-pointer">
                    <td class="px-4 py-3.5 text-xs text-gray-600 whitespace-nowrap font-medium">{{ product.codigo_barra || "—" }}</td>
                    <td class="px-4 py-3.5">
                      <p class="max-w-[380px] truncate text-sm font-semibold text-gray-800">{{ product.nombre_producto }}</p>
                    </td>
                    <td class="px-4 py-3.5 text-right font-bold text-gray-800 whitespace-nowrap">{{ formatCurrency(product.precio_unitario) }}</td>
                    <td class="px-4 py-3.5 text-center">
                      <span :class="[
                        'text-xs font-semibold px-2.5 py-0.5 rounded-full',
                        product.cantidad_producto <= 5 ? 'bg-red-100 text-red-700' : 
                        product.cantidad_producto <= 10 ? 'bg-amber-100 text-amber-700' : 
                        'bg-emerald-100 text-emerald-700'
                      ]">
                        {{ product.cantidad_producto }}
                      </span>
                    </td>
                    <td class="px-4 py-3.5 text-center">
                      <span :class="[
                        'inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold',
                        product.estado ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'
                      ]">
                        {{ product.estado ? "Activo" : "Inactivo" }}
                      </span>
                    </td>
                    <td class="px-4 py-3.5 text-center">
                      <button @click.stop="agregarDesdeModal(product)" :disabled="!product.estado || product.cantidad_producto <= 0" :class="[
                        'px-3.5 py-1.5 text-xs font-bold text-white rounded-lg transition-colors duration-200 shadow-sm hover:shadow',
                        product.cantidad_producto == 0 ? 'bg-red-500 cursor-not-allowed hover:bg-red-600' : 'bg-emerald-600 hover:bg-emerald-700',
                        !product.estado ? 'bg-gray-400 cursor-not-allowed' : ''
                      ]">
                        {{ product.cantidad_producto == 0 ? "Agotado" : "Agregar" }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="modalPagination && modalPagination.total > 0 && !modalLoading" class="mt-5 pt-4 border-t-2 border-gray-200">
              <div class="flex items-center justify-between flex-wrap gap-3">
                <div class="text-xs font-medium text-gray-500">
                  Mostrando {{ (modalPagination.currentPage - 1) * modalPageSize + 1 }} - {{ Math.min(modalPagination.currentPage * modalPageSize, modalPagination.total) }} de {{ modalPagination.total }} productos
                </div>
                <div class="flex gap-2">
                  <button @click="cambiarPaginaModal(modalPagination.currentPage - 1)" :disabled="modalPagination.currentPage === 1" class="px-3.5 py-1.5 text-xs font-semibold border-2 border-gray-300 rounded-lg hover:bg-gray-100 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
                    Anterior
                  </button>
                  <span class="px-3 py-1.5 text-xs font-semibold text-gray-600">Página {{ modalPagination.currentPage }} de {{ modalPagination.totalPages }}</span>
                  <button @click="cambiarPaginaModal(modalPagination.currentPage + 1)" :disabled="modalPagination.currentPage === modalPagination.totalPages" class="px-3.5 py-1.5 text-xs font-semibold border-2 border-gray-300 rounded-lg hover:bg-gray-100 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
                    Siguiente
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="px-6 py-4 border-t-2 border-gray-200 bg-gray-50 flex justify-between items-center flex-shrink-0">
          <p class="text-xs font-medium text-gray-500">Doble click para agregar</p>
          <button @click="closeProductModal" class="px-5 py-2 text-xs font-bold text-white bg-gray-800 rounded-lg hover:bg-gray-900 transition-colors duration-200 shadow-sm hover:shadow">
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { list_producto } from "../../productos/api/producto.ts";
import { create_venta, producto_list_x_codigo } from "../api/venta";
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
  playBeep,
} from "../utils/utils.ts";

export default {
  name: "POSVentas",

  data() {
    return {
      PAYMENT_CODES,

      cart: [],

      showProductModal: false,
      modalSearchTerm: "",
      modalProducts: [],
      modalLoading: false,
      modalSearchTimeout: null,
      modalPagination: null,
      modalCurrentPage: 1,
      modalPageSize: 10,

      selectedPaymentMethod: null,
      payments: [],
      cashAmount: null,
      cashAmountText: "",
      yapeAmount: null,
      yapeAmountText: "",
      procesandoVenta: false,
      isPaymentInputFocused: false,

      totals: {
        subtotal: 0,
        igvTotal: 0,
        total: 0,
        totalPaid: 0,
        remainingBalance: 0,
        totalVuelto: 0,
      },

      codigoEscaneado: "",
      escaneoTimeout: null,
      lastKeyTime: null,
      escaneando: false,
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
          return data.user?.nombre || "Administrador";
        }

        return "Administrador";
      } catch (error) {
        return "Administrador";
      }
    },

    subtotal() {
      return this.totals.subtotal;
    },

    igvTotal() {
      return this.totals.igvTotal;
    },

    total() {
      return this.totals.total;
    },

    totalPaid() {
      return this.totals.totalPaid;
    },

    remainingBalance() {
      return this.totals.remainingBalance;
    },

    totalVuelto() {
      return this.totals.totalVuelto;
    },

    totalRecibido() {
      return this.payments.reduce(
        (sum, p) => sum + (p.received || p.amount),
        0
      );
    },

    getCurrentAmount() {
      if (this.selectedPaymentMethod === PAYMENT_CODES.CASH) {
        return this.cashAmount || 0;
      }

      if (this.selectedPaymentMethod === PAYMENT_CODES.YAPE) {
        return this.yapeAmount || 0;
      }

      return 0;
    },

    getStatusClass() {
      const amount = this.getCurrentAmount;

      if (!amount || amount <= 0) return "";

      if (amount < this.remainingBalance) {
        return "bg-red-50/60 border-red-200/60";
      }

      if (amount === this.remainingBalance) {
        return "bg-emerald-50/60 border-emerald-200/60";
      }

      if (this.selectedPaymentMethod === PAYMENT_CODES.CASH) {
        return "bg-emerald-50/60 border-emerald-200/60";
      }

      return "bg-red-50/60 border-red-200/60";
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
    },
  },

  watch: {
    cart: {
      deep: true,
      handler() {
        this.updateTotals();
      },
    },

    payments: {
      deep: true,
      handler() {
        this.updateTotals();
      },
    },
  },

  mounted() {
    this.updateTotals();
    window.addEventListener("keydown", this.handleKeydown);
    window.addEventListener("paste", this.handlePaste);
  },

  beforeUnmount() {
    this.limpiarEscaner();
  },

  methods: {
    formatCurrency,

    limpiarEscaner() {
      window.removeEventListener("keydown", this.handleKeydown);
      window.removeEventListener("paste", this.handlePaste);

      if (this.modalSearchTimeout) {
        clearTimeout(this.modalSearchTimeout);
        this.modalSearchTimeout = null;
      }

      if (this.escaneoTimeout) {
        clearTimeout(this.escaneoTimeout);
        this.escaneoTimeout = null;
      }

      this.codigoEscaneado = "";
      this.lastKeyTime = null;
      this.escaneando = false;
    },

    isProductActive(product) {
      return (
        product.estado === true ||
        product.estado === "true" ||
        product.estado === 1
      );
    },

    onPaymentInputFocus() {
      this.isPaymentInputFocused = true;
    },

    onPaymentInputBlur() {
      this.isPaymentInputFocused = false;
    },

    handlePaste(event) {
      const target = event.target;

      if (this.showProductModal) {
        event.preventDefault();

        const pastedText = event.clipboardData?.getData("text") || "";

        if (pastedText) {
          this.modalSearchTerm = pastedText.trim();
          this.handleModalSearch();
        }

        return;
      }

      const isPaymentInput =
        target.tagName === "INPUT" &&
        (target.classList.contains("payment-input") ||
          target.placeholder?.toLowerCase().includes("monto") ||
          target.placeholder?.toLowerCase().includes("recibido"));

      if (isPaymentInput) {
        return;
      }

      const pastedText = event.clipboardData?.getData("text") || "";

      if (pastedText) {
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
        const isModalSearchInput =
          this.$refs.modalSearchInput && target === this.$refs.modalSearchInput;

        if (isModalSearchInput) {
          return;
        }

        return;
      }

      if (this.isPaymentInputFocused) {
        return;
      }

      const isPaymentInput =
        target.tagName === "INPUT" &&
        (target.classList.contains("payment-input") ||
          target.placeholder?.toLowerCase().includes("monto") ||
          target.placeholder?.toLowerCase().includes("recibido"));

      if (isPaymentInput) {
        return;
      }

      if (event.ctrlKey && event.key === "v") {
        return;
      }

      const now = Date.now();

      if (this.lastKeyTime && now - this.lastKeyTime > 300) {
        this.codigoEscaneado = "";
      }

      this.lastKeyTime = now;

      if (
        event.key.length === 1 &&
        !event.ctrlKey &&
        !event.altKey &&
        !event.metaKey
      ) {
        this.codigoEscaneado += event.key;

        if (this.escaneoTimeout) {
          clearTimeout(this.escaneoTimeout);
        }

        this.escaneoTimeout = setTimeout(() => {
          if (this.codigoEscaneado.trim()) {
            this.procesarEscaneo();
          }
        }, 150);
      }

      if (
        (event.key === "Enter" || event.key === "Tab") &&
        this.codigoEscaneado.trim()
      ) {
        event.preventDefault();

        if (this.escaneoTimeout) {
          clearTimeout(this.escaneoTimeout);
          this.escaneoTimeout = null;
        }

        this.procesarEscaneo();
      }
    },

    async procesarEscaneo() {
      if (this.escaneando) {
        return;
      }

      const codigo = this.codigoEscaneado.trim();

      if (!codigo) {
        this.codigoEscaneado = "";
        return;
      }

      this.escaneando = true;

      const codigoProcesar = codigo;
      this.codigoEscaneado = "";

      try {
        await this.buscarProductoPorCodigo(codigoProcesar);
      } finally {
        this.escaneando = false;
      }
    },

    async buscarProductoPorCodigo(codigoBarra) {
      if (!codigoBarra || codigoBarra.trim() === "") {
        return false;
      }

      try {
        const response = await producto_list_x_codigo(codigoBarra, "true");
        const producto = response.data;

        if (!producto || !producto.id) {
          showErrorAlert(`Producto no encontrado: ${codigoBarra}`);
          playBeep();
          return false;
        }

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

        const existingItem = this.cart.find((item) => item.id === producto.id);

        if (existingItem) {
          if (existingItem.quantity < producto.cantidad_producto) {
            existingItem.quantity++;

            showToast(
              `"${producto.nombre_producto}" cantidad aumentada a ${existingItem.quantity}`,
              "success"
            );

            playBeep();
          } else {
            showInsufficientStockAlert(
              producto.nombre_producto,
              producto.cantidad_producto
            );

            playBeep();
          }
        } else {
          this.agregarProductoAlCarrito(producto);

          showToast(
            `"${producto.nombre_producto}" agregado al carrito`,
            "success"
          );

          playBeep();
        }

        return true;
      } catch (error) {
        if (error.response && error.response.status === 404) {
          showErrorAlert(`Producto no encontrado: ${codigoBarra}`);
        } else {
          console.error("Error en búsqueda:", error);
          showErrorAlert("Error al buscar el producto");
        }

        playBeep();
        return false;
      }
    },

    agregarProductoAlCarrito(producto) {
      const existing = this.cart.find((item) => item.id === producto.id);

      if (existing) {
        if (existing.quantity < producto.cantidad_producto) {
          existing.quantity++;
        } else {
          showInsufficientStockAlert(
            producto.nombre_producto,
            producto.cantidad_producto
          );
        }
      } else {
        this.cart.push({ ...producto, quantity: 1 });
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

    updateQuantity(index, delta) {
      const item = this.cart[index];
      const newQty = item.quantity + delta;

      if (newQty <= 0) {
        this.cart.splice(index, 1);
      } else if (newQty <= item.cantidad_producto) {
        item.quantity = newQty;
      } else {
        showInsufficientStockAlert(
          item.nombre_producto,
          item.cantidad_producto
        );
      }
    },

    removeFromCart(index) {
      this.cart.splice(index, 1);
    },

    updateTotals() {
      const baseTotals = calculateTotals(this.cart);
      this.totals = updatePaymentCalculations(baseTotals, this.payments);
    },

    togglePaymentMethod(method) {
      if (this.selectedPaymentMethod === method) {
        this.selectedPaymentMethod = null;
        this.cashAmount = null;
        this.cashAmountText = "";
        this.yapeAmount = null;
        this.yapeAmountText = "";
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
      if (
        this.selectedPaymentMethod === PAYMENT_CODES.YAPE &&
        this.remainingBalance > 0
      ) {
        const amount = this.remainingBalance;

        this.yapeAmount = amount;
        this.yapeAmountText = amount.toString();
        this.addPaymentYape();

        showToast(
          `Pago Yape automático de ${formatCurrency(amount)} registrado`,
          "success"
        );
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
        console.error("Error actualizando monto Yape:", error);
        this.yapeAmount = 0;
        this.yapeAmountText = "0";
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
        console.error("Error actualizando monto efectivo:", error);
        this.cashAmount = 0;
        this.cashAmountText = "0";
      }
    },

    addPayment() {
      if (!this.selectedPaymentMethod) {
        showErrorAlert("Seleccione un método de pago");
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
        showErrorAlert("Ingrese un monto válido");
        return;
      }

      if (amount > this.remainingBalance) {
        showErrorAlert(
          `El monto no puede exceder el saldo pendiente (${formatCurrency(this.remainingBalance)})`
        );
        return;
      }

      amount = roundToTwoDecimals(amount) || 0;

      const payment = createYapePayment(amount);

      this.payments.push(payment);

      this.yapeAmount = null;
      this.yapeAmountText = "";
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
        changeAmount,
        received: amount,
        date: new Date().toLocaleTimeString(),
      };

      this.payments.push(payment);

      this.cashAmount = null;
      this.cashAmountText = "";
      this.selectedPaymentMethod = null;

      if (this.remainingBalance <= 0) {
        showPaymentCompletedAlert(this.totalPaid, this.totalVuelto);
      }
    },

    removePayment(index) {
      if (confirm("¿Estás seguro de eliminar este pago?")) {
        this.payments.splice(index, 1);
        showToast("Pago eliminado", "info");
      }
    },

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
    },

    closeProductModal() {
      this.showProductModal = false;
      this.modalSearchTerm = "";
      this.modalProducts = [];
      this.modalPagination = null;

      if (this.modalSearchTimeout) {
        clearTimeout(this.modalSearchTimeout);
      }
    },

    handleModalSearch() {
      if (this.modalSearchTimeout) {
        clearTimeout(this.modalSearchTimeout);
      }

      this.modalSearchTimeout = setTimeout(() => {
        this.cargarProductosModal(1);
      }, 400);
    },

    async cargarProductosModal(page = 1) {
      this.modalLoading = true;
      this.modalCurrentPage = page;

      try {
        const params = {
          page,
          page_size: this.modalPageSize,
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
            totalPages: Math.ceil(
              (response.data.count || 0) / this.modalPageSize
            ),
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
      if (!this.isProductActive(product)) {
        showProductInactiveAlert(product.nombre_producto);
        return;
      }

      if (product.cantidad_producto <= 0) {
        showNoStockAlert(product.nombre_producto);
        return;
      }

      const existing = this.cart.find((item) => item.id === product.id);

      if (existing) {
        if (existing.quantity < product.cantidad_producto) {
          existing.quantity++;
          showToast(`Cantidad aumentada: ${product.nombre_producto}`, "success");
        } else {
          showInsufficientStockAlert(
            product.nombre_producto,
            product.cantidad_producto
          );
        }
      } else {
        this.cart.push({ ...product, quantity: 1 });

        showToast(
          `"${product.nombre_producto}" agregado al carrito`,
          "success"
        );
      }

      playBeep();
    },

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
        const detalles = this.cart.map((item) => ({
          descripcion_producto: item.nombre_producto,
          codigo_barra: item.codigo_barra || "",
          codigo_interno: item.codigo_interno || "",
          cantidad_venta: item.quantity,
          producto_id: item.id,
          precio_venta: parseFloat(item.precio_unitario),
          sub_total_venta: parseFloat(
            (item.precio_unitario * item.quantity).toFixed(2)
          ),
        }));

        const pagos = this.payments.map((payment) => {
          const pago = {
            forma_pago: payment.method,
            monto_pagar: payment.amount,
          };

          if (payment.method === PAYMENT_CODES.CASH) {
            pago.efectivo_recibido = payment.received || payment.amount;
            pago.efectivo_vuelto = payment.changeAmount || 0;
          }

          return pago;
        });

        const response = await create_venta({
          id_usuario_venta: this.idUsuarioVenta,
          detalles,
          pagos,
        });

        if (response.data.success) {
          await showSaleCompletedAlert(response.data.correlativo, this.total);

          this.cart = [];
          this.payments = [];
          this.selectedPaymentMethod = null;
          this.cashAmount = null;
          this.cashAmountText = "";
          this.yapeAmount = null;
          this.yapeAmountText = "";
        } else {
          showSaleErrorAlert("Error al registrar la venta");
        }
      } catch (error) {
        console.error("Error al registrar venta:", error);
        showSaleErrorAlert("Error al registrar la venta");
      } finally {
        this.procesandoVenta = false;
      }
    },
  },
};
</script>
