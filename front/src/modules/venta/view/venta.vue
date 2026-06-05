<template>
  <div class="h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex flex-col">
    <!-- Header Separado - Sticky -->
    <div class="bg-white border-b border-slate-200 px-6 py-4 sticky top-0 z-10 shadow-sm flex-shrink-0">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        <div>
          <h1 class="text-xl md:text-2xl font-bold text-slate-800 tracking-tight">POS Executive</h1>
          <p class="text-xs md:text-sm text-slate-500 mt-0.5">Sistema de punto de venta profesional</p>
        </div>
        
        <div class="flex items-center gap-6">
          <div class="text-right">
            <p class="text-xs text-slate-400 uppercase tracking-wide">Fecha</p>
            <p class="text-sm font-semibold text-slate-700">{{ currentDate }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Contenido Principal -->
    <div class="flex-1 px-6 py-4 min-h-0">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
        <!-- Panel Izquierdo: Buscador + Catálogo -->
        <div class="lg:col-span-2 flex flex-col gap-4 min-h-0">
          <!-- Card Escáner -->
          <div class="bg-white rounded-xl border border-slate-200 shadow-sm flex-shrink-0">
            <div class="px-5 py-3 border-b border-slate-100 bg-slate-50/50">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <div class="p-1.5 bg-slate-100 rounded-lg">
                    <svg class="w-4 h-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <h2 class="text-sm font-semibold text-slate-700">Escáner rápido</h2>
                </div>
                <button 
                  @click="toggleScanner"
                  :class="[
                    'px-3 py-1.5 text-xs font-medium rounded-lg transition-all',
                    isScanning ? 'bg-red-50 text-red-600 hover:bg-red-100 border border-red-200' : 'bg-slate-800 text-white hover:bg-slate-700 shadow-sm'
                  ]"
                >
                  {{ isScanning ? 'Detener' : 'Activar cámara' }}
                </button>
              </div>
            </div>
            
            <div class="p-5">
              <div v-if="isScanning" style="display: none;">
                <div ref="scannerViewport"></div>
              </div>
              
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-4 w-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                  </svg>
                </div>
                <input 
                  v-model="searchTerm" 
                  @keyup.enter="handleSearch"
                  type="text" 
                  placeholder="Buscar por nombre o código... (Enter busca)"
                  class="w-full pl-9 pr-20 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-slate-300 focus:border-transparent"
                />
                <div class="absolute inset-y-0 right-0 flex items-center pr-1">
                  <button 
                    @click="handleSearch"
                    class="px-3 py-1 bg-slate-100 text-slate-700 text-xs font-medium rounded-md hover:bg-slate-200 transition-colors"
                  >
                    Buscar
                  </button>
                </div>
              </div>
              
              <div class="mt-3 flex items-center justify-between">
                <div v-if="isScanning" class="flex items-center gap-1.5 bg-green-50 px-2 py-0.5 rounded-full">
                  <div class="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></div>
                  <span class="text-xs text-green-700 font-medium">Escaneando</span>
                </div>
                <button 
                  v-if="searchTerm || filtroEstado !== 'todos'"
                  @click="limpiarFiltros"
                  class="text-xs text-slate-500 hover:text-slate-700"
                >
                  Limpiar filtros
                </button>
              </div>
            </div>
          </div>

          <!-- Catálogo de productos -->
          <div class="bg-white rounded-xl border border-slate-200 shadow-sm flex-1 flex flex-col overflow-hidden min-h-0">
            <div class="px-5 py-3 border-b border-slate-100 bg-slate-50/50 flex-shrink-0">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <div class="p-1.5 bg-slate-100 rounded-lg">
                    <svg class="w-4 h-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                  </div>
                  <h2 class="text-sm font-semibold text-slate-700">Catálogo de productos</h2>
                </div>
                <div class="flex items-center gap-2">
                  <select v-model="filtroEstado" @change="handleFilterChange" class="text-xs border border-slate-200 rounded-lg px-2 py-1 bg-white">
                    <option value="todos">Todos</option>
                    <option value="true">Activos</option>
                    <option value="false">Inactivos</option>
                  </select>
                  <span class="text-xs font-medium text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full">{{ pagination?.total || 0 }} productos</span>
                </div>
              </div>
            </div>
            
            <div class="flex-1 overflow-y-auto p-4">
              <div v-if="loading" class="flex items-center justify-center py-12">
                <div class="text-center">
                  <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-slate-800"></div>
                  <p class="mt-2 text-slate-500">Cargando productos...</p>
                </div>
              </div>
              
              <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div 
                  v-for="product in productos" 
                  :key="product.id"
                  @click="addToCart(product)"
                  :class="[
                    'group p-3 border rounded-lg cursor-pointer transition-all hover:shadow-sm',
                    product.estado === false || product.estado === 'false' 
                      ? 'border-red-100 bg-red-50/30 hover:bg-red-50/50' 
                      : 'border-slate-100 hover:bg-slate-50 hover:border-slate-200'
                  ]"
                >
                  <div class="flex justify-between items-start">
                    <div class="flex-1">
                      <p class="text-sm font-semibold text-slate-800">{{ product.nombre_producto }}</p>
                      <p class="text-xs text-slate-500 font-mono mt-1">Codigo barra: {{ product.codigo_barra || 'Sin código' }}</p>
                      <p class="text-xs text-slate-500 mt-1">Stock: {{ product.cantidad_producto }}</p>
                    </div>
                    <div class="text-right flex flex-col items-end gap-1">
                      <p class="text-sm font-bold text-slate-900">{{ formatCurrency(product.precio_unitario) }}</p>
                      <span 
                        :class="[
                          'text-xs px-2 py-0.5 rounded-full font-medium',
                          product.estado === false || product.estado === 'false'
                            ? 'bg-red-100 text-red-700'
                            : 'bg-green-100 text-green-700'
                        ]"
                      >
                        {{ product.estado === false || product.estado === 'false' ? 'Inactivo' : 'Activo' }}
                      </span>
                    </div>
                  </div>
                </div>
                <div v-if="productos.length === 0" class="col-span-2 text-center text-slate-400 py-12">
                  ✨ No se encontraron productos
                </div>
              </div>
            </div>

            <div v-if="pagination && pagination.total > 0 && !loading" class="px-5 py-3 border-t border-slate-100 bg-slate-50/50 flex-shrink-0">
              <div class="flex items-center justify-between flex-wrap gap-2">
                <div class="text-xs text-slate-500">
                  Mostrando {{ pagination.from }} - {{ pagination.to }} de {{ pagination.total }} productos
                </div>
                <div class="flex gap-2">
                  <button 
                    @click="cambiarPagina(pagination.previousPage)"
                    :disabled="!pagination.previousPage"
                    class="px-3 py-1 text-xs border rounded-lg hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    ← Anterior
                  </button>
                  <button 
                    @click="cambiarPagina(pagination.nextPage)"
                    :disabled="!pagination.nextPage"
                    class="px-3 py-1 text-xs border rounded-lg hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    Siguiente →
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Panel Derecho: Carrito -->
        <div class="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col overflow-hidden min-h-0">
          <div class="px-5 py-3 border-b border-slate-100 bg-slate-50/50 flex-shrink-0">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="p-1.5 bg-slate-100 rounded-lg">
                  <svg class="w-4 h-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-1.5 6M17 13l1.5 6M9 21h6M12 15v6"></path>
                  </svg>
                </div>
                <h2 class="text-sm font-semibold text-slate-700">Carrito de compra</h2>
              </div>
              <span class="text-xs font-medium bg-slate-100 px-2 py-0.5 rounded-full">{{ cart.length }} items</span>
            </div>
          </div>

          <div class="flex-1 overflow-y-auto p-4 space-y-3">
            <div v-for="(item, index) in cart" :key="item.id" class="bg-slate-50 rounded-lg p-3 hover:shadow-sm transition-shadow">
              <div class="flex justify-between items-start mb-2">
                <div class="flex-1">
                  <p class="text-sm font-semibold text-slate-800">{{ item.nombre_producto }}</p>
                  <p class="text-xs text-slate-400 font-mono">{{ item.codigo_barra || 'Sin código' }}</p>
                </div>
                <button @click="removeFromCart(index)" class="text-slate-400 hover:text-red-500 transition-colors ml-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </div>
              <div class="flex justify-between items-center">
                <div class="flex items-center gap-3">
                  <button @click="updateQuantity(index, -1)" class="w-7 h-7 rounded-lg border border-slate-200 bg-white text-slate-600 hover:bg-slate-100 text-sm font-medium">−</button>
                  <span class="text-sm font-semibold text-slate-800 min-w-[30px] text-center">{{ item.quantity }}</span>
                  <button @click="updateQuantity(index, 1)" class="w-7 h-7 rounded-lg border border-slate-200 bg-white text-slate-600 hover:bg-slate-100 text-sm font-medium">+</button>
                </div>
                <div class="text-right">
                  <p class="text-sm font-bold text-slate-900">{{ formatCurrency(item.precio_unitario * item.quantity) }}</p>
                  <p class="text-xs text-slate-400">P.U: {{ formatNumberExact(item.precio_unitario) }}</p>
                </div>
              </div>
            </div>
            
            <div v-if="cart.length === 0" class="text-center text-slate-400 py-12">
              <svg class="w-12 h-12 mx-auto mb-3 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-1.5 6M17 13l1.5 6M9 21h6M12 15v6"></path>
              </svg>
              <p class="text-sm">Carrito vacío</p>
              <p class="text-xs mt-1">Escanea o busca productos</p>
            </div>
          </div>

          <div class="border-t border-slate-200 p-4 space-y-3 bg-slate-50/30 flex-shrink-0">
            <div class="space-y-1.5">
              <div class="flex justify-between text-sm">
                <span class="text-slate-500">Subtotal</span>
                <span class="text-slate-700 font-medium">{{ formatCurrency(subtotal) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-slate-500">IGV (0%)</span>
                <span class="text-slate-700 font-medium">{{ formatCurrency(igvTotal) }}</span>
              </div>
              <div class="flex justify-between pt-2 border-t border-slate-200">
                <span class="text-base font-bold text-slate-900">Total</span>
                <span class="text-base font-bold text-slate-900">{{ formatCurrency(total) }}</span>
              </div>
            </div>
            
            <button 
              @click="processSale"
              :disabled="cart.length === 0 || procesandoVenta"
              class="w-full py-2 bg-slate-800 text-white text-sm font-semibold rounded-lg hover:bg-slate-700 transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ procesandoVenta ? 'Procesando...' : (cart.length === 0 ? 'Carrito vacío' : 'Procesar venta') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Pago -->
    <div v-if="showPaymentModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center p-6 border-b sticky top-0 bg-white rounded-t-2xl">
          <div>
            <h3 class="text-xl font-semibold text-slate-900">Registrar pagos</h3>
            <p class="text-sm text-slate-500 mt-1">Selecciona el método de pago para completar la venta</p>
          </div>
          <button @click="closePaymentModal" class="text-slate-400 hover:text-slate-600 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <div class="p-6">
          <div class="bg-gradient-to-r from-slate-50 to-slate-100 rounded-xl p-5 mb-6">
            <div class="flex justify-between items-center mb-3 pb-3 border-b border-slate-200">
              <span class="text-slate-600 text-sm font-medium">Total de la compra</span>
              <span class="text-2xl font-bold text-slate-900">{{ formatCurrency(total) }}</span>
            </div>
            <div class="flex justify-between items-center">
              <div>
                <span class="text-slate-600 text-sm font-medium">Pago pendiente</span>
                <div class="text-3xl font-bold mt-1" :class="remainingBalance > 0 ? 'text-amber-600' : 'text-emerald-600'">
                  {{ formatCurrency(remainingBalance) }}
                </div>
              </div>
              <div class="text-right">
                <span class="text-slate-500 text-xs">Pagado</span>
                <div class="text-lg font-semibold text-slate-700">{{ formatCurrency(totalPaid) }}</div>
              </div>
            </div>
          </div>

          <div v-if="payments.length > 0" class="mb-6">
            <h4 class="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
              <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
              Pagos realizados
            </h4>
            <div class="space-y-2">
              <div v-for="(payment, idx) in payments" :key="idx" class="flex justify-between items-center bg-slate-50 p-3 rounded-xl border border-slate-100">
                <div class="flex items-center gap-3">
                  <div :class="[
                    'w-8 h-8 rounded-full flex items-center justify-center',
                    payment.method === PAYMENT_CODES.YAPE ? 'bg-purple-100' : 'bg-green-100'
                  ]">
                    <span class="text-sm font-bold" :class="payment.method === PAYMENT_CODES.YAPE ? 'text-purple-600' : 'text-green-600'">
                      {{ payment.method === PAYMENT_CODES.YAPE ? 'Y' : 'S/' }}
                    </span>
                  </div>
                  <div>
                    <span :class="[
                      'text-sm font-medium',
                      payment.method === PAYMENT_CODES.YAPE ? 'text-purple-700' : 'text-green-700'
                    ]">
                      {{ getPaymentLabel(payment.method) }}
                    </span>
                    <p class="text-xs text-slate-400">
                      {{ payment.date || new Date().toLocaleTimeString() }}
                    </p>
                  </div>
                  <span class="font-bold text-slate-800 ml-2">{{ formatCurrency(payment.amount) }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span v-if="payment.method === PAYMENT_CODES.CASH && payment.changeAmount > 0" class="text-xs text-emerald-600 font-medium">
                    Vuelto: {{ formatCurrency(payment.changeAmount) }}
                  </span>
                  <button @click="removePayment(idx)" class="text-slate-400 hover:text-red-500 transition-colors p-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div v-if="remainingBalance > 0" class="border-t pt-5">
            <h4 class="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
              <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
              </svg>
              Agregar pago
            </h4>
            
            <div class="flex gap-3 mb-6">
              <button 
                v-for="method in paymentMethods"
                :key="method.value"
                @click="selectedPaymentMethod = method.value"
                :class="[
                  'flex-1 py-3 px-4 rounded-xl font-semibold transition-all border-2',
                  selectedPaymentMethod === method.value 
                    ? method.color + ' text-white border-transparent shadow-md' 
                    : 'bg-white text-slate-700 border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                ]"
              >
                <div class="flex items-center justify-center gap-2">
                  <span class="text-lg">{{ method.icon }}</span>
                  {{ method.label }}
                </div>
              </button>
            </div>

            <!-- Formulario Yape -->
            <div v-if="selectedPaymentMethod === PAYMENT_CODES.YAPE" class="text-center">
              <div class="mb-4">
                <label class="block text-sm font-medium text-slate-700 mb-2 text-left">Monto a pagar con {{ getPaymentLabel(PAYMENT_CODES.YAPE) }} (S/)</label>
                <div class="relative">
                  <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 font-medium">S/</span>
                  <input 
                    :value="yapeAmountText"
                    @input="updateYapeAmount"
                    type="text"
                    inputmode="decimal"
                    class="w-full pl-8 pr-3 py-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg font-semibold font-mono"
                    placeholder="0.00"
                  >
                </div>
                <div class="flex gap-2 mt-2">
                  <button @click="setYapeAmount(remainingBalance)" class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-lg hover:bg-blue-200 transition">{{ QUICK_BUTTON_LABELS.PAY_ALL }}</button>
                </div>
              </div>
              <button 
                @click="addPaymentYape"
                :disabled="!yapeAmount || yapeAmount <= 0 || yapeAmount > remainingBalance"
                class="w-full py-3 bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-xl hover:from-purple-700 hover:to-purple-800 transition-all font-semibold shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span class="flex items-center justify-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                  </svg>
                  Pagar {{ formatCurrency(yapeAmount || 0) }} con {{ getPaymentLabel(PAYMENT_CODES.YAPE) }}
                </span>
              </button>
            </div>

            <!-- Formulario Efectivo -->
            <div v-if="selectedPaymentMethod === PAYMENT_CODES.CASH" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">{{ getPaymentLabel(PAYMENT_CODES.CASH) }} - Monto recibido (S/)</label>
                <div class="relative">
                  <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 font-medium">S/</span>
                  <input 
                    :value="cashAmountText"
                    @input="updateCashAmount"
                    type="text"
                    inputmode="decimal"
                    class="w-full pl-8 pr-3 py-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent text-lg font-semibold font-mono"
                    placeholder="0.00"
                  >
                </div>
                <div class="flex gap-2 mt-2 flex-wrap">
                  <button 
                    @click="setCashAmount(remainingBalance)" 
                    class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-lg hover:bg-green-200 transition"
                  >
                    {{ QUICK_BUTTON_LABELS.PAY_ALL }}
                  </button>
                  <button 
                    v-for="amount in QUICK_CASH_AMOUNTS" 
                    :key="amount"
                    @click="setCashAmount(Math.min(amount, remainingBalance))" 
                    class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-lg hover:bg-green-200 transition"
                  >
                    {{ QUICK_BUTTON_LABELS.QUICK_AMOUNT(amount) }}
                  </button>
                </div>
              </div>
              
              <div v-if="cashAmount && cashAmount > 0" class="rounded-xl p-4" :class="isCashPaymentComplete ? 'bg-emerald-50' : 'bg-amber-50'">
                <div class="flex justify-between items-center">
                  <div>
                    <p class="text-sm font-medium" :class="isCashPaymentComplete ? 'text-emerald-800' : 'text-amber-800'">
                      {{ isCashPaymentComplete ? 'Vuelto del cliente' : 'Monto a pagar' }}
                    </p>
                    <p class="text-2xl font-bold mt-1" :class="isCashPaymentComplete ? 'text-emerald-600' : 'text-amber-600'">
                      {{ formatCurrency(calculateCashDifference) }}
                    </p>
                  </div>
                  <div class="text-right">
                    <p class="text-xs text-slate-500">Recibido: {{ formatCurrency(cashAmount || 0) }}</p>
                    <p class="text-xs text-slate-500">Saldo: {{ formatCurrency(remainingBalance) }}</p>
                  </div>
                </div>
              </div>
              
              <button 
                @click="addPaymentEfectivo"
                :disabled="!cashAmount || cashAmount <= 0"
                class="w-full py-3 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-xl hover:from-green-700 hover:to-green-800 transition-all font-semibold shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span class="flex items-center justify-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                  </svg>
                  {{ cashAmount >= remainingBalance ? 'Registrar pago' : 'Registrar pago' }}
                </span>
              </button>
            </div>
          </div>

          <div v-if="remainingBalance <= 0" class="bg-gradient-to-r from-emerald-50 to-green-50 p-5 rounded-xl text-center mt-4 border border-emerald-200">
            <svg class="w-12 h-12 text-emerald-600 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <p class="text-emerald-800 font-semibold text-lg">¡Pago completado!</p>
            <p class="text-sm text-emerald-600 mt-1">Total pagado: {{ formatCurrency(totalPaid) }}</p>
            <p v-if="totalVuelto > 0" class="text-sm text-emerald-600 font-medium mt-2">
              Vuelto total: {{ formatCurrency(totalVuelto) }}
            </p>
          </div>
        </div>

        <div class="p-6 border-t bg-slate-50 flex justify-end gap-3 rounded-b-2xl">
          <button 
            @click="closePaymentModal"
            class="px-5 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-100 rounded-xl transition"
          >
            Cancelar
          </button>
          <button 
            @click="finalizeSale"
            :disabled="remainingBalance > 0 || procesandoVenta"
            class="px-6 py-2.5 text-sm font-semibold text-white bg-slate-800 hover:bg-slate-700 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
          >
            {{ procesandoVenta ? 'Registrando...' : 'Finalizar compra' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { list_producto } from '../../productos/api/producto.ts';
import { create_venta } from '../api/venta';
import Quagga from '@ericblade/quagga2';
import {
  PAYMENT_CODES,
  QUICK_CASH_AMOUNTS,
  QUICK_BUTTON_LABELS,
  MAX_YAPE_AMOUNT,
  formatCurrency,
  formatNumberDisplay,
  formatNumberExact,
  roundToTwoDecimals,
  sanitizeCurrencyInput,
  parseCurrencyInput,
  calculateTotals,
  updatePaymentCalculations,
  calculateCashDifference,
  isCashPaymentComplete,
  createYapePayment,
  createEfectivoPayment,
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
  validateYapePayment,
  validateEfectivoPayment,
  getPaymentMethods,
  getPaymentLabel,
  getCurrentDateFormatted,
  playBeep
} from '../utils/utils.ts';

export default {
  name: "POSVentas",
  data() {
    return {
      // Constantes expuestas al template
      PAYMENT_CODES,
      QUICK_CASH_AMOUNTS,
      QUICK_BUTTON_LABELS,
      MAX_YAPE_AMOUNT,
      
      // Estado
      productos: [],
      cart: [],
      searchTerm: "",
      filtroEstado: "todos",
      isScanning: false,
      loading: false,
      quaggaInitialized: false,
      scanTimeout: null,
      scannerViewport: null,
      pagination: null,
      showPaymentModal: false,
      selectedPaymentMethod: PAYMENT_CODES.YAPE,
      payments: [],
      cashAmount: null,
      cashAmountText: '',
      yapeAmount: null,
      yapeAmountText: '',
      procesandoVenta: false,
      paymentMethods: getPaymentMethods(),
      totals: {
        subtotal: 0,
        igvTotal: 0,
        total: 0,
        totalPaid: 0,
        remainingBalance: 0,
        totalVuelto: 0
      }
    };
  },
  computed: {
    currentDate() {
      return getCurrentDateFormatted();
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
    calculateCashDifference() {
      return calculateCashDifference(this.cashAmount, this.remainingBalance);
    },
    isCashPaymentComplete() {
      return isCashPaymentComplete(this.cashAmount, this.remainingBalance);
    },
    totalVuelto() {
      return this.totals.totalVuelto;
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
        console.error("Error leyendo usuario:", error);
        return 1;
      }
    }
  },
  watch: {
    cart: {
      deep: true,
      handler() {
        this.updateTotals();
      }
    },
    payments: {
      deep: true,
      handler() {
        this.updateTotals();
      }
    }
  },
  mounted() {
    this.cargarProductos();
    this.updateTotals();
  },
  beforeDestroy() {
    if (this.isScanning) {
      this.stopScanner();
    }
  },
  methods: {
    formatCurrency,
    formatNumberDisplay,
    formatNumberExact,
    getPaymentLabel,
    
    updateTotals() {
      const baseTotals = calculateTotals(this.cart);
      this.totals = updatePaymentCalculations(baseTotals, this.payments);
    },
    
    updateYapeAmount(event) {
      const value = event.target.value;
      const sanitized = sanitizeCurrencyInput(value);
      this.yapeAmountText = sanitized;
      this.yapeAmount = parseCurrencyInput(sanitized);
    },
    
    updateCashAmount(event) {
      const value = event.target.value;
      const sanitized = sanitizeCurrencyInput(value);
      this.cashAmountText = sanitized;
      this.cashAmount = parseCurrencyInput(sanitized);
    },
    
    setCashAmount(amount) {
      const roundedAmount = roundToTwoDecimals(amount);
      this.cashAmount = roundedAmount;
      this.cashAmountText = roundedAmount !== null && !isNaN(roundedAmount) 
        ? roundedAmount.toString() 
        : '';
    },
    
    setYapeAmount(amount) {
      const roundedAmount = roundToTwoDecimals(amount);
      this.yapeAmount = roundedAmount;
      this.yapeAmountText = roundedAmount !== null && !isNaN(roundedAmount) 
        ? roundedAmount.toString() 
        : '';
    },
    
    async cargarProductos(params = {}) {
      this.loading = true;
      try {
        const defaultParams = {};
        if (this.filtroEstado !== 'todos') {
          defaultParams.estado = this.filtroEstado;
        }
        if (this.searchTerm) {
          defaultParams.search = this.searchTerm;
        }
        
        const finalParams = { ...defaultParams, ...params };
        const response = await list_producto(finalParams);
        
        if (response.data && response.data.results) {
          this.productos = response.data.results;
          this.pagination = {
            count: response.data.count || 0,
            next: response.data.next,
            previous: response.data.previous,
            nextPage: response.data.next,
            previousPage: response.data.previous,
            total: response.data.count || 0,
            from: this.pagination?.from || 1,
            to: response.data.results.length
          };
          
          const currentPage = finalParams.page || 1;
          const pageSize = 10;
          this.pagination.from = (currentPage - 1) * pageSize + 1;
          this.pagination.to = Math.min(currentPage * pageSize, this.pagination.total);
        } else {
          this.productos = [];
          this.pagination = null;
        }
      } catch (error) {
        console.error("Error cargando productos:", error);
        showErrorAlert('Error al cargar productos', 'Error de carga');
        this.productos = [];
      } finally {
        this.loading = false;
      }
    },
    
    async cambiarPagina(url) {
      if (!url) return;
      this.loading = true;
      try {
        const urlParams = new URL(url);
        const params = Object.fromEntries(urlParams.searchParams);
        const response = await list_producto(params);
        
        if (response.data && response.data.results) {
          this.productos = response.data.results;
          this.pagination = {
            count: response.data.count || 0,
            next: response.data.next,
            previous: response.data.previous,
            nextPage: response.data.next,
            previousPage: response.data.previous,
            total: response.data.count || 0,
            from: this.pagination?.from || 1,
            to: response.data.results.length
          };
        }
      } catch (error) {
        console.error("Error cambiando página:", error);
        showErrorAlert('Error al cambiar de página', 'Error');
      } finally {
        this.loading = false;
      }
    },
    
    handleSearch() {
      this.cargarProductos({ page: 1 });
    },
    
    handleFilterChange() {
      this.cargarProductos({ page: 1 });
    },
    
    limpiarFiltros() {
      this.searchTerm = "";
      this.filtroEstado = "todos";
      this.cargarProductos({ page: 1 });
    },
    
    async startScanner() {
      if (this.quaggaInitialized) {
        try {
          Quagga.offDetected(this.onDetected);
          Quagga.stop();
        } catch (err) {}
        this.quaggaInitialized = false;
      }

      if (!this.scannerViewport) {
        showErrorAlert('Error al iniciar el escáner', 'Error');
        this.isScanning = false;
        return;
      }

      try {
        await Quagga.init({
          inputStream: {
            type: 'LiveStream',
            target: this.scannerViewport,
            constraints: { width: { min: 640 }, height: { min: 480 }, facingMode: 'environment' },
          },
          locator: { patchSize: 'medium', halfSample: true },
          numOfWorkers: navigator.hardwareConcurrency || 4,
          decoder: { readers: ['code_128_reader', 'ean_reader', 'ean_8_reader', 'code_39_reader', 'upc_reader', 'upc_e_reader', 'codabar_reader'] },
          locate: true,
          frequency: 5,
        });
        Quagga.start();
        this.quaggaInitialized = true;
        Quagga.onDetected(this.onDetected);
      } catch (err) {
        console.error('Error al iniciar escáner:', err);
        showErrorAlert('No se pudo acceder a la cámara', 'Error de cámara');
        this.isScanning = false;
      }
    },
    
    onDetected(result) {
      if (!this.isScanning || this.scanTimeout) return;
      const code = result.codeResult.code;
      this.searchTerm = code;
      this.handleSearch();
      showToast(`🔍 Buscando producto con código: ${code}`, 'info');
      playBeep();
      this.scanTimeout = setTimeout(() => { this.scanTimeout = null; }, 1000);
    },
    
    stopScanner() {
      if (this.quaggaInitialized) {
        Quagga.offDetected(this.onDetected);
        Quagga.stop();
        this.quaggaInitialized = false;
      }
      this.isScanning = false;
      if (this.scanTimeout) clearTimeout(this.scanTimeout);
    },
    
    async toggleScanner() {
      if (this.isScanning) {
        this.stopScanner();
      } else {
        this.isScanning = true;
        await this.$nextTick();
        this.scannerViewport = this.$refs.scannerViewport;
        await this.startScanner();
      }
    },
    
    addToCart(product) {
      if (product.estado === false || product.estado === 'false') {
        showProductInactiveAlert(product.nombre_producto);
        return;
      }
      
      const existing = this.cart.find(item => item.id === product.id);
      if (existing) {
        if (existing.quantity < product.cantidad_producto) {
          existing.quantity++;
        } else {
          showInsufficientStockAlert(product.nombre_producto, product.cantidad_producto);
        }
      } else {
        if (product.cantidad_producto > 0) {
          this.cart.push({ ...product, quantity: 1 });
        } else {
          showNoStockAlert(product.nombre_producto);
        }
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
        showInsufficientStockAlert(item.nombre_producto, item.cantidad_producto);
      }
    },
    
    removeFromCart(index) {
      this.cart.splice(index, 1);
    },
    
    async processSale() {
      if (this.cart.length === 0) {
        showEmptyCartAlert();
        return;
      }
      this.showPaymentModal = true;
      this.payments = [];
      this.setCashAmount(null);
      this.setYapeAmount(null);
      this.selectedPaymentMethod = PAYMENT_CODES.YAPE;
    },
    
    addPaymentYape() {
      let amount = this.yapeAmount;
      
      const validation = validateYapePayment(amount, this.remainingBalance, this.maxYapeAmount);
      if (!validation.valid) {
        showErrorAlert(validation.errorMessage || 'Monto inválido', 'Monto inválido');
        return;
      }
      
      amount = roundToTwoDecimals(amount) || 0;
      const payment = createYapePayment(amount);
      this.payments.push(payment);
      this.setYapeAmount(null);
      
      if (this.remainingBalance <= 0) {
        showPaymentCompletedAlert(this.totalPaid, this.totalVuelto);
      }
    },
    
    addPaymentEfectivo() {
      let amount = this.cashAmount;
      
      const validation = validateEfectivoPayment(amount);
      if (!validation.valid) {
        showInvalidAmountAlert();
        return;
      }
      
      amount = roundToTwoDecimals(amount) || 0;
      const payment = createEfectivoPayment(amount, this.remainingBalance);
      this.payments.push(payment);
      this.setCashAmount(null);
      
      if (this.remainingBalance <= 0) {
        showPaymentCompletedAlert(this.totalPaid, this.totalVuelto);
      }
    },
    
    removePayment(index) {
      this.payments.splice(index, 1);
    },
    
    closePaymentModal() {
      this.showPaymentModal = false;
      this.payments = [];
      this.setCashAmount(null);
      this.setYapeAmount(null);
    },
    
    async finalizeSale() {
      if (this.remainingBalance > 0) {
        showIncompletePaymentAlert(this.remainingBalance);
        return;
      }
      
      if (this.procesandoVenta) {
        return;
      }
      
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
          detalles: detalles,
          pagos: pagos
        });
        
        if (response.data.success) {
          await showSaleCompletedAlert(response.data.correlativo, this.total);
          this.cart = [];
          this.closePaymentModal();
          this.cargarProductos();
        } else {
          showSaleErrorAlert('Error al registrar la venta');
        }
        
      } catch (error) {
        console.error('Error al registrar venta:', error);
        let errorMsg = 'Error al registrar la venta';
        if (error.response?.data) {
          errorMsg = JSON.stringify(error.response.data);
        }
        showSaleErrorAlert(errorMsg);
      } finally {
        this.procesandoVenta = false;
      }
    }
  }
};
</script>