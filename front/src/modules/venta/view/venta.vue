<template>
  <div class="h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col">
    <!-- Header Rediseñado -->
    <header class="bg-white border-b border-gray-200 px-8 py-6">
      <div class="flex justify-between items-start">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center flex-shrink-0">
            <span class="text-white text-sm font-bold">V</span>
          </div>
          <div>
            <h1 class="text-base sm:text-xl font-semibold text-gray-800 tracking-tight">Punto de Venta</h1>
            <p class="text-xs text-gray-500 hidden sm:block">Sistema de gestión de ventas</p>
          </div>
        </div>
        <div class="flex gap-3">
          <div class="text-right">
            <p class="text-xs text-gray-500">{{ currentDate }}</p>
            <p class="text-xs font-medium text-gray-700">{{ nombreUsuario }}</p>
          </div>
        </div>
      </div>
    </header>

    <!-- Contenido Principal -->
    <main class="flex-1 px-4 sm:px-6 md:px-8 py-4 sm:py-6 min-h-0 overflow-y-auto">
      <div class="flex flex-col lg:flex-row gap-4 md:gap-6 lg:gap-8 h-full">
        
        <!-- Panel Izquierdo: Catálogo -->
        <div class="flex-1 lg:w-[70%] lg:flex-none flex flex-col gap-4 md:gap-5 min-h-[650px] lg:min-h-0">
          
          <!-- Buscador rediseñado -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200/60 flex-shrink-0 overflow-hidden">
            <div class="px-4 sm:px-6 py-3 sm:py-4 bg-gray-50/50 border-b border-gray-200/60">
              <h2 class="text-sm font-semibold text-gray-700 flex items-center gap-2">
                <span class="w-1 h-4 bg-gray-900 rounded-full"></span>
                Buscar producto
              </h2>
            </div>
            
            <div class="p-4 sm:p-5">
              <div class="relative group">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-4 w-4 text-gray-400 group-focus-within:text-gray-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <input 
                  ref="searchInput"
                  v-model="searchTerm" 
                  @input="handleManualSearch"
                  type="text" 
                  placeholder="Escriba para buscar productos..."
                  class="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-gray-400 focus:ring-2 focus:ring-gray-200 transition-all bg-gray-50/30"
                />
              </div>
              
              <div class="mt-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <button 
                  v-if="searchTerm || filtroEstado !== 'todos'"
                  @click="limpiarFiltros"
                  class="text-xs text-gray-500 hover:text-gray-700 transition-colors flex items-center gap-1 order-2 sm:order-1"
                >
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  Limpiar filtros
                </button>
                
                <div class="flex items-center gap-3 order-1 sm:order-2">
                  <select v-model="filtroEstado" @change="handleFilterChange" class="text-xs border border-gray-200 rounded-lg px-3 py-1.5 bg-white text-gray-700 focus:outline-none focus:border-gray-400">
                    <option value="todos">Todos los productos</option>
                    <option value="true">Activos</option>
                    <option value="false">Inactivos</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <!-- Catálogo de productos rediseñado -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200/60 flex-1 flex flex-col overflow-hidden transition-all hover:shadow-md">
            <div class="px-4 sm:px-6 py-3 sm:py-4 bg-gray-50/50 border-b border-gray-200/60 flex-shrink-0">
              <div class="flex items-center justify-between">
                <h2 class="text-sm font-semibold text-gray-700 flex items-center gap-2">
                  <span class="w-1 h-4 bg-gray-900 rounded-full"></span>
                  Catálogo de productos
                </h2>
                <span class="text-xs text-gray-500 bg-white px-2.5 py-1 rounded-full shadow-sm">{{ pagination?.total || 0 }} productos</span>
              </div>
            </div>
            
            <div class="flex-1 overflow-y-auto p-4 sm:p-5">
              <div v-if="loading" class="flex items-center justify-center py-16">
                <div class="text-center">
                  <div class="inline-block animate-spin rounded-full h-8 w-8 border-2 border-gray-300 border-t-gray-600"></div>
                  <p class="mt-3 text-sm text-gray-500">Cargando productos...</p>
                </div>
              </div>
              
              <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
                <div 
                  v-for="product in productos" 
                  :key="product.id"
                  @click="addToCart(product)"
                  :class="[
                    'group p-3 sm:p-4 rounded-xl cursor-pointer transition-all duration-200 transform hover:-translate-y-0.5',
                    product.estado === false || product.estado === 'false' 
                      ? 'border-red-200 bg-red-50/30 hover:shadow-md hover:border-red-300' 
                      : 'border border-gray-200 hover:shadow-md hover:border-gray-300 bg-white'
                  ]"
                >
                  <div class="flex justify-between items-start gap-2">
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-semibold text-gray-800 group-hover:text-gray-900 transition-colors truncate">{{ product.nombre_producto }}</p>
                      <p class="text-xs text-gray-500 mt-1.5">Código barra: {{ product.codigo_barra || '---' }}</p>
                      <div class="mt-2 flex items-center gap-2">
                        <span class="text-xs text-gray-500 flex-shrink-0">Stock:</span>
                        <span :class="[
                          'text-xs font-medium px-2 py-0.5 rounded-full',
                          product.cantidad_producto <= 5 ? 'bg-yellow-100 text-yellow-700' : 'bg-gray-100 text-gray-600'
                        ]">
                          {{ product.cantidad_producto }} unidades
                        </span>
                      </div>
                    </div>
                    <div class="text-right flex-shrink-0">
                      <p class="text-base font-bold text-gray-900">{{ formatCurrency(product.precio_unitario) }}</p>
                      <span 
                        :class="[
                          'text-xs px-2 py-0.5 rounded-full mt-2 inline-block',
                          product.estado === false || product.estado === 'false'
                            ? 'bg-red-100 text-red-600'
                            : 'bg-green-100 text-green-600'
                        ]"
                      >
                        {{ product.estado === false || product.estado === 'false' ? 'Inactivo' : 'Activo' }}
                      </span>
                    </div>
                  </div>
                </div>
                <div v-if="productos.length === 0" class="col-span-2 text-center py-16">
                  <svg class="w-12 h-12 text-gray-300 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                  </svg>
                  <p class="text-gray-400 text-sm">No se encontraron productos</p>
                </div>
              </div>
            </div>

            <div v-if="pagination && pagination.total > 0 && !loading" class="px-4 sm:px-6 py-3 border-t border-gray-200/60 bg-gray-50/30 flex-shrink-0">
              <div class="flex items-center justify-between flex-wrap gap-2">
                <div class="text-xs text-gray-500">
                  Mostrando {{ pagination.from }} - {{ pagination.to }} de {{ pagination.total }}
                </div>
                <div class="flex gap-2">
                  <button 
                    @click="cambiarPagina(pagination.previousPage)"
                    :disabled="!pagination.previousPage"
                    class="px-3 py-1.5 text-xs border border-gray-200 rounded-lg hover:bg-white hover:border-gray-300 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                    Anterior
                  </button>
                  <button 
                    @click="cambiarPagina(pagination.nextPage)"
                    :disabled="!pagination.nextPage"
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

        <!-- Panel Derecho: Carrito rediseñado -->
        <div class="flex-1 lg:w-[30%] lg:flex-none flex flex-col min-h-[650px] lg:min-h-0">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200/60 flex flex-col overflow-hidden transition-all hover:shadow-md h-full">
            <div class="px-4 sm:px-6 py-3 sm:py-4 bg-gray-50/50 border-b border-gray-200/60 flex-shrink-0">
              <div class="flex items-center justify-between">
                <h2 class="text-sm font-semibold text-gray-700 flex items-center gap-2">
                  <span class="w-1 h-4 bg-gray-900 rounded-full"></span>
                  Carrito de compras
                </h2>
                <span class="text-xs text-gray-500 bg-white px-2.5 py-1 rounded-full shadow-sm">{{ cart.length }} items</span>
              </div>
            </div>

            <div class="flex-1 overflow-y-auto p-3 sm:p-5 space-y-3">
              <div v-for="(item, index) in cart" :key="item.id" class="bg-white border border-gray-200 rounded-xl p-3 shadow-sm hover:shadow-md transition-all">
                <div class="flex justify-between items-start mb-3 gap-2">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-semibold text-gray-800 truncate">{{ item.nombre_producto }}</p>
                    <p class="text-xs text-gray-400 font-mono mt-0.5 truncate">{{ item.codigo_barra || 'Sin código' }}</p>
                  </div>
                  <button @click="removeFromCart(index)" class="text-gray-400 hover:text-red-500 transition-colors p-1 flex-shrink-0">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                <div class="flex justify-between items-center gap-2">
                  <div class="flex items-center gap-2 bg-gray-50 rounded-lg p-1">
                    <button @click="updateQuantity(index, -1)" class="w-7 h-7 sm:w-8 sm:h-8 rounded-md border border-gray-200 bg-white text-gray-600 hover:bg-gray-100 transition-colors text-sm font-medium flex items-center justify-center">−</button>
                    
                    <input 
                      type="number"
                      :value="item.quantity"
                      @input="updateQuantityManually(index, $event)"
                      min="1"
                      :max="item.cantidad_producto"
                      class="text-sm font-semibold text-gray-800 w-12 text-center border-0 focus:outline-none focus:ring-0 bg-transparent [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                    />
                    
                    <button @click="updateQuantity(index, 1)" class="w-7 h-7 sm:w-8 sm:h-8 rounded-md border border-gray-200 bg-white text-gray-600 hover:bg-gray-100 transition-colors text-sm font-medium flex items-center justify-center">+</button>
                  </div>
                  <div class="text-right flex-shrink-0">
                    <p class="text-sm font-bold text-gray-900">{{ formatCurrency(item.precio_unitario * item.quantity) }}</p>
                    <p class="text-xs text-gray-400">P.U: {{ formatNumberExact(item.precio_unitario) }}</p>
                  </div>
                </div>
              </div>
              
              <div v-if="cart.length === 0" class="text-center py-16">
                <svg class="w-16 h-16 text-gray-200 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                <p class="text-gray-400 text-sm">Carrito vacío</p>
                <p class="text-xs text-gray-300 mt-1">Seleccione productos del catálogo</p>
              </div>
            </div>

            <div class="border-t border-gray-200/60 p-4 sm:p-5 space-y-3 sm:space-y-4 bg-gradient-to-r from-gray-50 to-white flex-shrink-0">
              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">Subtotal</span>
                  <span class="text-gray-700 font-medium">{{ formatCurrency(subtotal) }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">IGV (0%)</span>
                  <span class="text-gray-700 font-medium">{{ formatCurrency(igvTotal) }}</span>
                </div>
                <div class="flex justify-between pt-2 sm:pt-3 border-t border-gray-200">
                  <span class="text-sm sm:text-base font-bold text-gray-900">Total a pagar</span>
                  <span class="text-sm sm:text-base font-bold text-gray-900">{{ formatCurrency(total) }}</span>
                </div>
              </div>
              
              <button 
                @click="processSale"
                :disabled="cart.length === 0 || procesandoVenta"
                class="w-full py-2.5 bg-gray-800 text-white text-sm font-semibold rounded-xl hover:bg-gray-700 transition-all transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 shadow-md"
              >
                {{ procesandoVenta ? 'Procesando...' : (cart.length === 0 ? 'Carrito vacío' : 'Procesar venta') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal de Pago Rediseñado -->
    <div v-if="showPaymentModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-2 sm:p-4">
      <div class="bg-white rounded-2xl shadow-2xl max-w-5xl w-full max-h-[95vh] sm:max-h-[90vh] flex flex-col overflow-hidden animate-fadeInUp">
        
        <!-- Header -->
        <div class="px-4 sm:px-7 py-4 sm:py-5 border-b border-gray-100 flex justify-between items-center bg-white">
          <div>
            <h3 class="text-lg sm:text-xl font-semibold text-gray-900">Registrar pago</h3>
          </div>
          <button @click="closePaymentModal" class="text-gray-400 hover:text-gray-600 text-2xl leading-none transition-colors w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100">
            ×
          </button>
        </div>

        <!-- Contenido -->
        <div class="flex-1 overflow-y-auto p-4 sm:p-7 bg-gray-50/50">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-8">
            
            <!-- Resumen del carrito mejorado -->
            <div class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
              <div class="bg-gray-50/80 px-4 sm:px-5 py-2 sm:py-3 border-b border-gray-200">
                <h4 class="text-sm font-semibold text-gray-700">Detalles de compra</h4>
              </div>
              <div class="p-3 sm:p-4 space-y-2 max-h-[350px] overflow-y-auto">
                <div v-for="(item, idx) in cart" :key="idx" class="flex justify-between text-sm py-2 border-b border-gray-100 last:border-0">
                  <div class="flex-1">
                    <span class="text-gray-700 font-medium">{{ item.nombre_producto }}</span>
                    <span class="text-gray-400 ml-2 text-xs">x{{ item.quantity }}</span>
                  </div>
                  <span class="text-gray-800 font-semibold">{{ formatCurrency(item.precio_unitario * item.quantity) }}</span>
                </div>
              </div>
              <div class="bg-gray-50 px-4 sm:px-5 py-2 sm:py-3 border-t border-gray-200 flex justify-between font-bold text-gray-900">
                <span>Total</span>
                <span>{{ formatCurrency(total) }}</span>
              </div>
            </div>

            <!-- Flujo de pago uniforme mejorado -->
            <div class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
              
              <!-- Paso 1: Selección de método -->
              <div v-if="!selectedPaymentMethod && remainingBalance > 0" class="p-4 sm:p-5">
                <h4 class="text-sm font-semibold text-gray-700 mb-4">Seleccionar método de pago</h4>
                <div class="space-y-3">
                  <button 
                    @click="selectPaymentMethod(PAYMENT_CODES.CASH)"
                    class="w-full p-3 sm:p-4 border-2 border-gray-200 rounded-xl text-left hover:border-gray-300 hover:bg-gray-50 transition-all"
                  >
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 bg-green-50 rounded-full flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <div>
                        <span class="font-semibold text-gray-800">Efectivo</span>
                        <p class="text-xs text-gray-500 mt-0.5 hidden sm:block">Pago con billetes y monedas</p>
                      </div>
                    </div>
                  </button>
                  
                  <button 
                    @click="selectPaymentMethod(PAYMENT_CODES.YAPE)"
                    class="w-full p-3 sm:p-4 border-2 border-gray-200 rounded-xl text-left hover:border-gray-300 hover:bg-gray-50 transition-all"
                  >
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 bg-blue-50 rounded-full flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <circle cx="12" cy="12" r="8" stroke-width="1.5"/>
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 8L12 12L16 8M12 12L12 18" />
                        </svg>
                      </div>
                      <div>
                        <span class="font-semibold text-gray-800">Yape</span>
                        <p class="text-xs text-gray-500 mt-0.5 hidden sm:block">Pago mediante Yape</p>
                      </div>
                    </div>
                  </button>
                </div>
              </div>

              <!-- Paso 2: Formulario de pago uniforme -->
              <div v-else-if="selectedPaymentMethod && remainingBalance > 0" class="p-4 sm:p-5">
                <div class="flex items-center gap-3 mb-5">
                  <button @click="selectedPaymentMethod = null" class="text-gray-400 hover:text-gray-600 transition-colors p-1">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                  </button>
                  <h4 class="text-sm font-semibold text-gray-700">
                    {{ selectedPaymentMethod === PAYMENT_CODES.CASH ? 'Pago en efectivo' : 'Pago con Yape' }}
                  </h4>
                </div>

                <div class="bg-gradient-to-r from-blue-50 to-gray-50 rounded-xl p-4 mb-5 border border-blue-100">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-600">Saldo pendiente:</span>
                    <span class="text-xl sm:text-2xl font-bold text-red-500">{{ formatCurrency(remainingBalance) }}</span>
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-2">
                    {{ selectedPaymentMethod === PAYMENT_CODES.CASH ? 'Monto recibido' : 'Monto a pagar con Yape' }}
                  </label>
                  <input 
                    :ref="selectedPaymentMethod === PAYMENT_CODES.CASH ? 'cashInput' : 'yapeInput'"
                    :value="selectedPaymentMethod === PAYMENT_CODES.CASH ? cashAmountText : yapeAmountText"
                    @input="selectedPaymentMethod === PAYMENT_CODES.CASH ? updateCashAmount($event) : updateYapeAmount($event)"
                    type="text"
                    inputmode="decimal"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-base sm:text-lg font-mono focus:outline-none focus:border-gray-400 focus:ring-2 focus:ring-gray-200 transition-all"
                    placeholder="0.00"
                  >
                </div>

                <div v-if="getCurrentAmount > 0" class="mt-5 rounded-xl p-4 text-center" :class="getStatusClass">
                  <div v-if="getCurrentAmount < remainingBalance">
                    <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Falta por pagar</p>
                    <p class="text-xl sm:text-2xl font-bold text-red-600">{{ formatCurrency(remainingBalance - getCurrentAmount) }}</p>
                    <p class="text-xs text-gray-500 mt-2">
                      Monto ingresado: {{ formatCurrency(getCurrentAmount) }}
                    </p>
                  </div>
                  
                  <div v-else-if="getCurrentAmount === remainingBalance">
                    <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Pago completado</p>
                    <p class="text-sm font-medium text-green-600">No hay saldo pendiente</p>
                  </div>
                  
                  <div v-else-if="selectedPaymentMethod === PAYMENT_CODES.CASH">
                    <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">Vuelto</p>
                    <p class="text-xl sm:text-2xl font-bold text-green-600">{{ formatCurrency(getCurrentAmount - remainingBalance) }}</p>
                    <p class="text-xs text-gray-500 mt-2">
                      Recibido: {{ formatCurrency(getCurrentAmount) }} | Total: {{ formatCurrency(remainingBalance) }}
                    </p>
                  </div>
                </div>

                <div class="space-y-3 mt-5">
                  <button 
                    @click="addPayment"
                    :disabled="!getCurrentAmount || getCurrentAmount <= 0"
                    class="w-full py-2.5 bg-gray-800 text-white rounded-xl font-semibold hover:bg-gray-700 transition-all disabled:opacity-50 shadow-md"
                  >
                    Registrar pago
                  </button>

                  <button 
                    @click="setFullPayment"
                    class="w-full py-2.5 border-2 border-gray-200 text-gray-700 rounded-xl font-medium text-sm hover:bg-gray-50 transition-all"
                  >
                    Pagar total ({{ formatCurrency(remainingBalance) }})
                  </button>
                </div>
              </div>

              <!-- Pagos registrados -->
              <div v-if="payments.length > 0" class="border-t border-gray-200 bg-gray-50">
                <div class="p-3 sm:p-4">
                  <h5 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
                    Pagos realizados (Total: {{ formatCurrency(totalPaid) }})
                  </h5>
                  <div class="space-y-2 max-h-[200px] overflow-y-auto">
                    <div v-for="(payment, idx) in payments" :key="idx" class="flex justify-between items-center text-sm p-2 sm:p-3 bg-white rounded-xl border border-gray-200 shadow-sm">
                      <div class="flex gap-2 sm:gap-3">
                        <span class="font-semibold text-gray-700">{{ payment.method === PAYMENT_CODES.YAPE ? 'Yape' : 'Efectivo' }}</span>
                        <span class="text-gray-400 text-xs">{{ payment.date }}</span>
                      </div>
                      <div class="flex items-center gap-2">
                        <span class="font-bold text-gray-900">{{ formatCurrency(payment.received || payment.amount) }}</span>
                        <button @click="removePayment(idx)" class="text-gray-400 hover:text-red-500 transition-colors p-1">
                          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- PAGO COMPLETADO -->
              <div v-if="remainingBalance <= 0" class="border-t border-gray-200 bg-gray-50 p-4 sm:p-5">
                <div class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
                  <div class="bg-gray-800 px-4 sm:px-5 py-2 sm:py-3">
                    <h4 class="text-xs sm:text-sm font-semibold text-white tracking-wide">COMPROBANTE DE PAGO</h4>
                  </div>
                  
                  <div class="p-4 sm:p-5 space-y-3 sm:space-y-4">
                    <div class="flex justify-between items-baseline pb-3 border-b border-gray-100">
                      <span class="text-xs sm:text-sm text-gray-500 uppercase tracking-wide">Total venta</span>
                      <span class="text-xl sm:text-2xl font-bold text-gray-900">{{ formatCurrency(total) }}</span>
                    </div>
                    
                    <div class="flex justify-between items-baseline pb-3 border-b border-gray-100">
                      <span class="text-xs sm:text-sm text-gray-500 uppercase tracking-wide">Monto recibido</span>
                      <span class="text-base sm:text-xl font-semibold text-gray-800">{{ formatCurrency(totalRecibido) }}</span>
                    </div>
                    
                    <div v-if="totalVuelto > 0" class="flex justify-between items-baseline pt-2">
                      <span class="text-xs sm:text-sm font-medium text-gray-600 uppercase tracking-wide">Vuelto</span>
                      <span class="text-xl sm:text-2xl font-bold text-green-600">{{ formatCurrency(totalVuelto) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-4 sm:px-7 py-3 sm:py-4 border-t border-gray-100 bg-white flex justify-end gap-3 rounded-b-2xl">
          <button 
            @click="closePaymentModal"
            class="px-4 sm:px-5 py-2 border-2 border-gray-200 text-gray-700 rounded-xl font-medium hover:bg-gray-50 transition-all text-sm sm:text-base"
          >
            Cancelar
          </button>
          <button 
            @click="finalizeSale"
            :disabled="remainingBalance > 0 || procesandoVenta"
            class="px-5 sm:px-6 py-2 bg-green-600 text-white rounded-xl font-semibold hover:bg-green-700 transition-all transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 shadow-md text-sm sm:text-base"
          >
            {{ remainingBalance > 0 ? `Faltan ${formatCurrency(remainingBalance)}` : (procesandoVenta ? 'Registrando...' : 'Finalizar venta') }}
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
/* Mejor experiencia táctil en móvil */
@media (max-width: 640px) {
  button, 
  [role="button"],
  .cursor-pointer {
    min-height: 44px;
    min-width: 44px;
  }
}

/* Animación del modal */
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

<script>
import { list_producto } from '../../productos/api/producto.ts';
import { create_venta } from '../api/venta';
import {
  PAYMENT_CODES,
  formatCurrency,
  formatNumberDisplay,
  formatNumberExact,
  roundToTwoDecimals,
  sanitizeCurrencyInput,
  parseCurrencyInput,
  calculateTotals,
  updatePaymentCalculations,
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
  getPaymentLabel,
  getCurrentDateFormatted,
  playBeep
} from '../utils/utils.ts';

export default {
  name: "POSVentas",
  data() {
    return {
      PAYMENT_CODES,
      
      productos: [],
      cart: [],
      searchTerm: "",
      filtroEstado: "todos",
      loading: false,
      pagination: null,
      showPaymentModal: false,
      selectedPaymentMethod: null,
      payments: [],
      cashAmount: null,
      cashAmountText: '',
      yapeAmount: null,
      yapeAmountText: '',
      procesandoVenta: false,
      totals: {
        subtotal: 0,
        igvTotal: 0,
        total: 0,
        totalPaid: 0,
        remainingBalance: 0,
        totalVuelto: 0
      },
      // Variables para capturar escaneo de pistola
      barcodeBuffer: '',
      barcodeTimeout: null,
      lastKeyTime: 0,
      isScanning: false
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
      return this.payments.reduce((sum, p) => sum + (p.received || p.amount), 0);
    },
    paymentProgress() {
      if (this.total === 0) return 0;
      return (this.totalPaid / this.total) * 100;
    },
    getCurrentAmount() {
      if (this.selectedPaymentMethod === PAYMENT_CODES.CASH) {
        return this.cashAmount || 0;
      } else if (this.selectedPaymentMethod === PAYMENT_CODES.YAPE) {
        return this.yapeAmount || 0;
      }
      return 0;
    },
    getStatusClass() {
      const amount = this.getCurrentAmount;
      if (!amount || amount <= 0) return '';
      if (amount < this.remainingBalance) return 'bg-red-50 border-red-200';
      if (amount === this.remainingBalance) return 'bg-green-50 border-green-200';
      if (this.selectedPaymentMethod === PAYMENT_CODES.CASH) return 'bg-green-50 border-green-200';
      return 'bg-red-50 border-red-200';
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
    payments: { deep: true, handler() { this.updateTotals(); } },
    // Debounce para búsqueda manual
    searchTerm() {
      this.handleManualSearch();
    }
  },
  mounted() {
    this.cargarProductos();
    this.updateTotals();
    // Escuchar eventos de teclado globales para capturar el escáner
    window.addEventListener('keydown', this.handleKeyDown);
    window.addEventListener('keyup', this.handleKeyUp);
  },
  beforeDestroy() {
    window.removeEventListener('keydown', this.handleKeyDown);
    window.removeEventListener('keyup', this.handleKeyUp);
    if (this.barcodeTimeout) clearTimeout(this.barcodeTimeout);
  },
  methods: {
    formatCurrency,
    formatNumberDisplay,
    formatNumberExact,
    getPaymentLabel,
    
    // Capturar teclas para detectar escaneo de pistola
    handleKeyDown(event) {
      // Ignorar si el foco está en un input (es escritura manual)
      const activeElement = document.activeElement;
      const isInputFocused = activeElement && (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA');
      
      // Si el usuario está escribiendo manualmente, no interferir
      if (isInputFocused) {
        return;
      }
      
      // Detectar si es un escaneo (teclas rápidas)
      const now = Date.now();
      const timeDiff = now - this.lastKeyTime;
      
      // Si la diferencia es menor a 50ms, es un escaneo rápido de pistola
      if (timeDiff < 50) {
        this.isScanning = true;
      }
      
      this.lastKeyTime = now;
      
      // Capturar la tecla presionada (solo caracteres imprimibles)
      if (event.key.length === 1 && !event.ctrlKey && !event.altKey && !event.metaKey) {
        // Prevenir que el carácter se escriba en cualquier lugar
        event.preventDefault();
        
        // Agregar al buffer del código de barras
        this.barcodeBuffer += event.key;
        
        // Reiniciar timeout para esperar el Enter
        if (this.barcodeTimeout) clearTimeout(this.barcodeTimeout);
        this.barcodeTimeout = setTimeout(() => {
          // Timeout alcanzado, probablemente no era un escaneo completo
          this.barcodeBuffer = '';
          this.isScanning = false;
        }, 100);
      }
      
      // Detectar la tecla Enter (fin del escaneo)
      if (event.key === 'Enter' && this.barcodeBuffer.length > 0) {
        event.preventDefault();
        
        // Procesar el código de barras
        const codigo = this.barcodeBuffer;
        this.barcodeBuffer = '';
        this.isScanning = false;
        
        if (this.barcodeTimeout) clearTimeout(this.barcodeTimeout);
        
        // Agregar el producto al carrito
        this.buscarProductoPorCodigo(codigo);
      }
    },
    
    handleKeyUp(event) {
      // No es necesario hacer nada aquí por ahora
    },
    
    // Búsqueda manual (solo filtra, no agrega al carrito)
    handleManualSearch() {
      // Usar debounce para no hacer muchas peticiones
      if (this.searchTimeout) clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.cargarProductos({ page: 1 });
      }, 500);
    },
    
    updateQuantityManually(index, event) {
      const item = this.cart[index];
      let newQuantity = parseInt(event.target.value);
      
      if (isNaN(newQuantity) || newQuantity < 1) {
        newQuantity = 1;
      }
      
      if (newQuantity > item.cantidad_producto) {
        newQuantity = item.cantidad_producto;
        showInsufficientStockAlert(item.nombre_producto, item.cantidad_producto);
      }
      
      item.quantity = newQuantity;
      
      if (newQuantity === 0) {
        this.cart.splice(index, 1);
      }
    },

    selectPaymentMethod(method) {
      this.selectedPaymentMethod = method;
      this.$nextTick(() => {
        if (method === PAYMENT_CODES.CASH && this.$refs.cashInput) {
          this.$refs.cashInput.focus();
        } else if (method === PAYMENT_CODES.YAPE && this.$refs.yapeInput) {
          this.$refs.yapeInput.focus();
        }
      });
    },
    
    setFullPayment() {
      if (this.selectedPaymentMethod === PAYMENT_CODES.CASH) {
        this.setCashAmount(this.remainingBalance);
      } else if (this.selectedPaymentMethod === PAYMENT_CODES.YAPE) {
        this.setYapeAmount(this.remainingBalance);
      }
    },
    
    updateTotals() {
      const baseTotals = calculateTotals(this.cart);
      this.totals = updatePaymentCalculations(baseTotals, this.payments);
    },
    
    updateYapeAmount(event) {
      const value = event.target.value;
      const sanitized = sanitizeCurrencyInput(value);
      this.yapeAmountText = sanitized;
      let amount = parseCurrencyInput(sanitized);
      
      if (amount > this.remainingBalance) {
        amount = this.remainingBalance;
        this.yapeAmountText = amount.toString();
        showToast(`El monto no puede exceder el saldo pendiente. Se ajustó a ${formatCurrency(amount)}`, 'warning');
      }
      
      this.yapeAmount = amount;
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
      this.cashAmountText = roundedAmount !== null && !isNaN(roundedAmount) ? roundedAmount.toString() : '';
    },
    
    setYapeAmount(amount) {
      const roundedAmount = roundToTwoDecimals(amount);
      this.yapeAmount = roundedAmount;
      this.yapeAmountText = roundedAmount !== null && !isNaN(roundedAmount) ? roundedAmount.toString() : '';
    },
    
    addPayment() {
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
      this.setYapeAmount(null);
      this.selectedPaymentMethod = null;
      
      if (this.remainingBalance <= 0) {
        showPaymentCompletedAlert(this.totalPaid, this.totalVuelto);
      } else {
        console.log(`Pago Yape registrado: ${formatCurrency(amount)}. Faltan: ${formatCurrency(this.remainingBalance)}`, 'success');
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
      this.setCashAmount(null);
      this.selectedPaymentMethod = null;
      
      if (this.remainingBalance <= 0) {
        showPaymentCompletedAlert(this.totalPaid, this.totalVuelto);
      } else {
        console.log(`Pago efectivo registrado: ${formatCurrency(paymentAmount)}. Recibido: ${formatCurrency(amount)}. Faltan: ${formatCurrency(this.remainingBalance)}`);
      }
    },
    
    removePayment(index) {
      this.payments.splice(index, 1);
    },
    
    closePaymentModal() {
      this.showPaymentModal = false;
      this.payments = [];
      this.selectedPaymentMethod = null;
      this.setCashAmount(null);
      this.setYapeAmount(null);
    },
    
    async cargarProductos(params = {}) {
      this.loading = true;
      try {
        const defaultParams = {};
        if (this.filtroEstado !== 'todos') defaultParams.estado = this.filtroEstado;
        if (this.searchTerm) defaultParams.search = this.searchTerm;
        
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
        showErrorAlert('Error al cargar productos');
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
        showErrorAlert('Error al cambiar de página');
      } finally {
        this.loading = false;
      }
    },
    
    handleFilterChange() { this.cargarProductos({ page: 1 }); },
    
    limpiarFiltros() {
      this.searchTerm = "";
      this.filtroEstado = "todos";
      this.cargarProductos({ page: 1 });
    },
    
    // Función para buscar producto por código de barras y agregarlo al carrito
    async buscarProductoPorCodigo(codigoBarra) {
      try {
        // Buscar el producto por código de barras
        const response = await list_producto({ 
          codigo_barra: codigoBarra,
          estado: 'true' // Solo productos activos
        });
        
        if (response.data && response.data.results && response.data.results.length > 0) {
          const producto = response.data.results[0];
          
          // Verificar si el producto está activo
          if (producto.estado === false || producto.estado === 'false') {
            showProductInactiveAlert(producto.nombre_producto);
            playBeep();
            return false;
          }
          
          // Verificar stock
          if (producto.cantidad_producto <= 0) {
            showNoStockAlert(producto.nombre_producto);
            playBeep();
            return false;
          }
          
          // Agregar al carrito
          this.agregarProductoAlCarrito(producto);
          playBeep(); // Sonido de éxito
          showToast(`✓ "${producto.nombre_producto}" agregado al carrito`, 'success');
          return true;
        } else {
          showErrorAlert(`No se encontró el producto con código: ${codigoBarra}`, 'Producto no encontrado');
          playBeep(); // Sonido de error
          return false;
        }
      } catch (error) {
        console.error("Error buscando producto por código:", error);
        showErrorAlert('Error al buscar el producto');
        return false;
      }
    },
    
    // Método auxiliar para agregar producto al carrito
    agregarProductoAlCarrito(producto) {
      const existing = this.cart.find(item => item.id === producto.id);
      
      if (existing) {
        if (existing.quantity < producto.cantidad_producto) {
          existing.quantity++;
          showToast(`Cantidad de "${producto.nombre_producto}" incrementada`, 'info');
        } else {
          showInsufficientStockAlert(producto.nombre_producto, producto.cantidad_producto);
        }
      } else {
        this.cart.push({ ...producto, quantity: 1 });
      }
    },
    
    // Método para agregar desde el catálogo (clic)
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
      this.selectedPaymentMethod = null;
      this.setCashAmount(null);
      this.setYapeAmount(null);
    },
    
    async finalizeSale() {
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
          const pago = { 
            forma_pago: payment.method, 
            monto_pagar: payment.amount 
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
        showSaleErrorAlert('Error al registrar la venta');
      } finally {
        this.procesandoVenta = false;
      }
    }
  }
};
</script>