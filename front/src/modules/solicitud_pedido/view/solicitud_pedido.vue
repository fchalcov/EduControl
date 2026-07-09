<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 px-4 sm:px-8 py-4 sm:py-6">
      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4 sm:gap-0">
        
        <!-- Logo y título -->
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center flex-shrink-0">
            <span class="text-white text-xs font-bold">C</span>
          </div>
          <div>
            <h1 class="text-base sm:text-xl font-semibold text-gray-800 tracking-tight">Gestión de Compras</h1>
            <p class="text-xs text-gray-500 hidden sm:block">Administración de solicitudes y abastecimiento</p>
          </div>
        </div>
        
        <!-- Botón -->
        <div class="flex gap-3">
          <button @click="abrirNuevaSolicitud"
            class="flex-1 sm:flex-none px-4 sm:px-5 py-2 text-xs font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 transition-colors flex items-center justify-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Nueva Solicitud
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="px-8 py-6">
      <!-- KPI Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg border border-gray-200 p-5">
          <div>
            <p class="text-xs font-medium text-gray-500  tracking-wide">Total Invertido</p>
            <p class="text-2xl font-bold text-gray-900 mt-2">S/ {{ formatNumber(totalInvertido) }}</p>
          </div>
        </div>

        <div class="bg-white rounded-lg border border-gray-200 p-5">
          <div>
            <p class="text-xs font-medium text-gray-500  tracking-wide">Órdenes Pendientes</p>
            <p class="text-2xl font-bold text-orange-600 mt-2">{{ totalPendientes }}</p>
          </div>
        </div>

        <div class="bg-white rounded-lg border border-gray-200 p-5">
          <div>
            <p class="text-xs font-medium text-gray-500  tracking-wide">Recepción Parcial</p>
            <p class="text-2xl font-bold text-blue-600 mt-2">{{ totalRecepciónParcial }}</p>
          </div>
        </div>

        <div class="bg-white rounded-lg border border-gray-200 p-5">
          <div>
            <p class="text-xs font-medium text-gray-500  tracking-wide">Completadas</p>
            <p class="text-2xl font-bold text-emerald-600 mt-2">{{ totalCompletadas }}</p>
          </div>
        </div>
      </div>

      <!-- Filters Panel -->
      <div class="bg-white rounded-lg border border-gray-200 mb-8">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-xs font-semibold text-gray-700 flex items-center gap-2">
            <span class="w-1 h-4 bg-gray-900 rounded-full"></span>
            Filtros de búsqueda
          </h2>
        </div>

        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4">
            <div>
              <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">N° Solicitud</label>
              <input v-model="filters.numero_solicitud" type="text" placeholder="PED-2026..."
                class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none">
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Proveedor</label>
              <select v-model="filters.proveedor"
                class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none bg-white">
                <option value="">Todos</option>
                <option value="1">Distribuidora del Sur</option>
                <option value="2">Importaciones García</option>
                <option value="3">Corporación López</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Estado</label>
              <select v-model="filters.estado"
                class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none bg-white">
                <option value="">Todos</option>
                <option value="1">Pendiente</option>
                <option value="2">Pedido enviado</option>
                <option value="3">Recibido parcial</option>
                <option value="4">Recibido completo</option>
                <option value="5">Anulada</option>
                <option value="6">Cerrada</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Fecha desde</label>
              <input v-model="filters.fecha_desde" type="date"
                class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none">
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Fecha hasta</label>
              <input v-model="filters.fecha_hasta" type="date"
                class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none">
            </div>

            <div class="flex items-end">
              <button @click="aplicarFiltros"
                class="w-full px-4 py-2 bg-gray-900 text-white text-xs font-medium rounded-lg hover:bg-gray-800 transition-colors">
                Buscar
              </button>
            </div>
          </div>

          <div v-if="filtrosActivos" class="mt-4 pt-4 border-t border-gray-100 flex items-center gap-2 flex-wrap">
            <span class="text-xs text-gray-500">Filtros activos:</span>
            <span v-if="filters.numero_solicitud"
              class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700">
              N°: {{ filters.numero_solicitud }}
            </span>
            <span v-if="filters.proveedor"
              class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700">
              Proveedor: {{ getProveedorNombre(parseInt(filters.proveedor)) }}
            </span>
            <span v-if="filters.estado"
              class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700">
              Estado: {{ getEstadoTexto(parseInt(filters.estado)) }}
            </span>
            <button @click="limpiarFiltros" class="text-xs text-red-400 hover:text-red-600 ml-2">
              Limpiar todo
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
        <p class="text-gray-500 mt-4">Cargando solicitudes...</p>
      </div>

      <!-- Solicitudes Table -->
      <div v-else class="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h2 class="text-xs font-semibold text-gray-700 flex items-center gap-2">
            <span class="w-1 h-4 bg-gray-900 rounded-full"></span>
            Solicitudes de Pedido
          </h2>
          <span class="text-xs text-gray-500">{{ solicitudesFiltradas.length }} resultados</span>
        </div>

        <div class="overflow-x-auto" v-if="solicitudesFiltradas.length > 0">
          <table class="w-full">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">N°
                  Solicitud</th>
                <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Proveedor
                </th>
                <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Fecha
                  Solicitud</th>
                <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Fecha
                  Requerida</th>
                <th class="text-right px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Total</th>
                <th class="text-right px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Recibido
                </th>
                <th class="text-right px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Pendiente
                </th>
                <th class="text-center px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Estado
                </th>
                <th class="text-center px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Acciones
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="solicitud in solicitudesPaginadas" :key="solicitud.id_solicitud"
                class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4">
                  <div class="text-xs font-semibold text-gray-900 font-mono">{{ solicitud.correlativo }}</div>
                </td>
                <td class="px-6 py-4">
                  <div class="text-xs text-gray-900">{{ solicitud.proveedor_nombre }}</div>
                  <div class="text-xs text-gray-400">{{ solicitud.numero_comprobante || 'Sin comprobante' }}</div>
                </td>
                <td class="px-6 py-4">
                  <div class="text-xs text-gray-900">{{ formatFechaShort(solicitud.fecha_solicitud) }}</div>
                  <div class="text-xs text-gray-400">{{ formatHora(solicitud.fecha_solicitud) }}</div>
                </td>
                <td class="px-6 py-4">
                  <div class="text-xs text-gray-900">{{ formatFechaShort(solicitud.fecha_requerida) }}</div>
                </td>
                <td class="px-6 py-4 text-right font-bold text-xs text-gray-900">
                  S/ {{ formatNumber(solicitud.total) }}
                </td>
                <td class="px-6 py-4 text-right text-xs text-emerald-600 font-semibold">
                  S/ {{ formatNumber(solicitud.total_recibido || 0) }}
                </td>
                <td class="px-6 py-4 text-right text-xs text-orange-600 font-semibold">
                  S/ {{ formatNumber((solicitud.total || 0) - (solicitud.total_recibido || 0)) }}
                </td>
                <td class="px-6 py-4 text-center">
                  <span :class="getEstadoClass(solicitud.estado)"
                    class="inline-block px-2.5 py-1 rounded-full text-xs font-medium">
                    {{ getEstadoTexto(solicitud.estado) }}
                  </span>
                </td>
                <td class="px-6 py-4 text-center">
                  <div class="flex justify-center gap-2">
                    <button @click="verDetalle(solicitud)"
                      class="text-xs font-medium text-gray-600 hover:text-blue-600 px-3 py-1.5 rounded-md hover:bg-blue-50 transition-all">
                      <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z">
                        </path>
                      </svg>
                      Ver
                    </button>
                    <button v-if="solicitud.estado !== 4 && solicitud.estado !== 5 && solicitud.estado !== 6"
                      @click="abrirRecepcion(solicitud)"
                      class="text-xs font-medium text-gray-600 hover:text-emerald-600 px-3 py-1.5 rounded-md hover:bg-emerald-50 transition-all">
                      <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                      </svg>
                      Recibir
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="text-center py-16">
          <p class="text-gray-500">No se encontraron solicitudes</p>
          <p class="text-xs text-gray-400 mt-1">Haz clic en "Nueva Solicitud" para comenzar</p>
        </div>

        <div class="px-6 py-4 border-t border-gray-200 flex justify-between items-center">
          <div class="text-xs text-gray-500">
            Mostrando {{ (currentPage - 1) * itemsPerPage + 1 }} - {{ Math.min(currentPage * itemsPerPage,
              solicitudesFiltradas.length) }} de {{ solicitudesFiltradas.length }} resultados
          </div>
          <div class="flex gap-2">
            <button @click="currentPage--" :disabled="currentPage === 1"
              class="px-3 py-1 text-xs border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              Anterior
            </button>
            <span class="px-3 py-1 text-xs bg-gray-100 rounded-lg">
              Página {{ currentPage }} de {{ totalPages }}
            </span>
            <button @click="currentPage++" :disabled="currentPage === totalPages"
              class="px-3 py-1 text-xs border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              Siguiente
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal Nueva Solicitud -->
    <div v-if="modalSolicitudVisible"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="cerrarModalSolicitud">
      <div class="bg-white rounded-xl w-full h-full flex flex-col overflow-hidden">
        <div class="border-b border-gray-200 px-6 py-5 flex justify-between items-center bg-white sticky top-0">
          <div>
            <h2 class="text-lg font-semibold text-gray-900">{{ solicitudEditando ? 'Editar Solicitud' : 'Nueva Solicitud' }}</h2>
            <p class="text-xs text-gray-500">Complete los datos del pedido</p>
          </div>
          <button @click="cerrarModalSolicitud"
            class="text-gray-400 hover:text-gray-600 text-2xl leading-none">✕</button>
        </div>

        <div class="flex-1 overflow-y-auto p-6">
          <form @submit.prevent="guardarSolicitud">
            <!-- Datos Generales -->
            <div class="mb-8">
              <h3 class="text-xs font-semibold text-gray-900 mb-4 border-l-3 border-gray-900 pl-3">Datos Generales</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Proveedor
                    *</label>
                  <select v-model="solicitudForm.proveedor_id" required
                    class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none bg-white">
                    <option value="">Seleccionar proveedor</option>
                    <option value="1">Distribuidora del Sur</option>
                    <option value="2">Importaciones García</option>
                    <option value="3">Corporación López</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Fecha Requerida
                    *</label>
                  <input v-model="solicitudForm.fecha_requerida" type="date" required
                    class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none">
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Forma de
                    Pago</label>
                  <select v-model="solicitudForm.forma_pago"
                    class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none bg-white">
                    <option value="1">Contado</option>
                    <option value="2">Crédito</option>
                    <option value="3">Mixto</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Tipo
                    Comprobante</label>
                  <select v-model="solicitudForm.tipo_comprobante"
                    class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none bg-white">
                    <option value="">Sin comprobante</option>
                    <option value="Factura">Factura</option>
                    <option value="Boleta">Boleta</option>
                    <option value="Guía">Guía de remisión</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">N°
                    Comprobante</label>
                  <input v-model="solicitudForm.numero_comprobante" type="text"
                    class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none"
                    placeholder="F001-00012345">
                </div>
                <div class="md:col-span-2 lg:col-span-4">
                  <label
                    class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Observaciones</label>
                  <textarea v-model="solicitudForm.observaciones" rows="2"
                    class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none"
                    placeholder="Notas adicionales..."></textarea>
                </div>
              </div>
            </div>

            <!-- Productos -->
            <div>
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-xs font-semibold text-gray-900 border-l-3 border-gray-900 pl-3">Productos</h3>
                <button type="button" @click="agregarProducto"
                  class="text-xs font-medium text-white bg-gray-900 px-3 py-1.5 rounded-lg hover:bg-gray-800">
                  + Agregar Producto
                </button>
              </div>

              <div class="overflow-x-auto border border-gray-200 rounded-lg">
                <table class="w-full text-xs">
                  <thead class="bg-gray-50 border-b border-gray-200">
                    <tr>
                      <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500  tracking-wider w-8">#</th>
                      <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500  tracking-wider min-w-[300px]">Producto *</th>
                      <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500  tracking-wider">Cantidad *</th>
                      <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500  tracking-wider">Precio Compra</th>
                      <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500  tracking-wider">Subtotal</th>
                      <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500  tracking-wider">Costo por Unidad</th>
                      <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500  tracking-wider">Precio Venta Sugerido</th>
                      <th class="text-center px-4 py-3 text-xs font-semibold text-gray-500  tracking-wider w-16">Acciones</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100">
                    <tr v-for="(producto, index) in solicitudForm.productos" :key="index" class="hover:bg-gray-50 transition-colors">
                      <td class="px-4 py-3 text-gray-500 text-center">{{ index + 1 }}</td>
                      <td class="px-4 py-3">
                        <div class="relative">
                          <input type="text" v-model="producto.buscador"
                            @input="buscarProductos(producto, $event.target.value)" @focus="mostrarResultados(producto)"
                            @blur="ocultarResultados(producto)" placeholder="Escribe para buscar producto..."
                            autocomplete="off"
                            class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none" />
                          <div
                            v-if="producto.mostrarResultados && producto.resultados && producto.resultados.length > 0"
                            class="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                            <div v-for="prod in producto.resultados" :key="prod.id"
                              @mousedown.prevent="seleccionarProducto(producto, prod)"
                              class="px-3 py-2 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-0">
                              <p class="text-xs font-medium text-gray-900">{{ prod.nombre }}</p>
                              <p class="text-xs text-gray-500">Código: {{ prod.codigo }} | Stock: {{ prod.stock }}</p>
                            </div>
                          </div>
                        </div>
                      </td>

                      <td class="px-4 py-3">
                        <div class="flex items-center gap-2">
                          <input v-model.number="producto.cantidad_paquetes" type="number" min="0" step="1"
                            :disabled="!producto.id_producto" @input="calcularProducto(producto)"
                            class="w-24 text-right px-2 py-1.5 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none disabled:bg-gray-50"
                            placeholder="0">
                          <span class="text-xs text-gray-600">Paq</span>
                          <span class="text-xs text-gray-400 mx-1">×</span>
                          <input v-model.number="producto.unidades_por_paquete" type="number" min="1" step="1"
                            :disabled="!producto.id_producto" @input="calcularProducto(producto)"
                            class="w-20 text-right px-2 py-1.5 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none disabled:bg-gray-50"
                            placeholder="1">
                          <span class="text-xs text-gray-600">Uni</span>
                        </div>
                      </td>

                      <td class="px-4 py-3">
                        <input v-model.number="producto.precio_paquete" type="number" min="0" step="0.01" required
                          :disabled="!producto.id_producto" @input="calcularProducto(producto)"
                          class="w-full text-right px-2 py-1.5 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none disabled:bg-gray-50"
                          placeholder="0.00">
                      </td>

                      <td class="px-4 py-3 text-right font-semibold text-gray-900">
                        S/ {{ formatNumber(producto.subtotal || 0) }}
                        <div class="text-xs text-gray-400">
                          ({{ producto.cantidad_paquetes || 0 }} paq × S/ {{ formatNumber(producto.precio_paquete) }})
                        </div>
                      </td>

                      <!-- Costo por Unidad (lo que realmente cuesta cada unidad) -->
                      <td class="px-4 py-3 text-right font-semibold text-gray-500">
                        S/ {{ formatNumber(producto.precio_venta_unidad || 0) }}
                        <div class="text-xs text-gray-400">costo por unidad</div>
                      </td>

                      <!-- Precio Venta Sugerido (editable) -->
                      <td class="px-4 py-3">
                        <input v-model.number="producto.precio_venta_editable" type="number" min="0" step="0.01"
                          :disabled="!producto.id_producto || producto.total_unidades === 0"
                          @input="calcularGanancia(producto)"
                          class="w-full text-right px-2 py-1.5 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none disabled:bg-gray-50"
                          placeholder="Precio de venta" />
                        <div class="text-xs text-gray-400 text-right">
                          Sugerido: S/ {{ formatNumber(producto.precio_sugerido || 0) }}
                        </div>
                      </td>

                      <td class="px-4 py-3 text-center">
                        <button type="button" @click="eliminarProducto(index)"
                          class="text-red-400 hover:text-red-600 transition-colors">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16">
                            </path>
                          </svg>
                        </button>
                      </td>
                    </tr>

                    <tr v-if="solicitudForm.productos.length === 0">
                      <td colspan="8" class="px-4 py-8 text-center text-gray-500">
                        No hay productos agregados
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </form>
        </div>

        <div class="border-t border-gray-200 px-6 py-4 bg-gray-50 flex justify-end gap-3 sticky bottom-0">
          <button @click="cerrarModalSolicitud"
            class="px-4 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            Cancelar
          </button>
          <button @click="guardarSolicitud"
            class="px-4 py-2 text-xs font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800">
            {{ solicitudEditando ? 'Actualizar' : 'Crear Solicitud' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Recepción de Productos -->
    <div v-if="modalRecepcionVisible"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="cerrarModalRecepcion">
      <div class="bg-white rounded-xl w-full max-w-6xl max-h-[90vh] flex flex-col overflow-hidden">
        <div class="border-b border-gray-200 px-6 py-5 flex justify-between items-center bg-white">
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Recepción de Productos</h2>
            <p class="text-xs text-gray-500 font-mono">{{ solicitudRecepcion?.correlativo }} - {{
              solicitudRecepcion?.proveedor_nombre }}</p>
          </div>
          <button @click="cerrarModalRecepcion"
            class="text-gray-400 hover:text-gray-600 text-2xl leading-none">✕</button>
        </div>

        <div class="flex-1 overflow-y-auto p-6">
          <div class="mb-6">
            <h3 class="text-xs font-semibold text-gray-900 mb-4">Productos pendientes por recibir</h3>
            <div class="overflow-x-auto border border-gray-200 rounded-lg">
              <table class="w-full text-xs">
                <thead class="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Producto</th>
                    <th class="text-right px-4 py-3 text-xs font-semibold text-gray-500">Pedido</th>
                    <th class="text-right px-4 py-3 text-xs font-semibold text-gray-500">Recibido</th>
                    <th class="text-right px-4 py-3 text-xs font-semibold text-gray-500">Pendiente</th>
                    <th class="text-right px-4 py-3 text-xs font-semibold text-gray-500">Precio Unit.</th>
                    <th class="text-right px-4 py-3 text-xs font-semibold text-gray-500 w-40">Cantidad a Recibir</th>
                    <th class="text-right px-4 py-3 text-xs font-semibold text-gray-500">Subtotal</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="detalle in solicitudRecepcion?.detalles" :key="detalle.id_detalle_solicitud">
                    <td class="px-4 py-3 font-medium text-gray-900">{{ detalle.nombre_producto }}</td>
                    <td class="px-4 py-3 text-right">{{ detalle.cantidad_pedida }}</td>
                    <td class="px-4 py-3 text-right text-emerald-600">{{ detalle.cantidad_recibida || 0 }}</td>
                    <td class="px-4 py-3 text-right text-orange-600">{{ detalle.cantidad_pedida -
                      (detalle.cantidad_recibida || 0) }}</td>
                    <td class="px-4 py-3 text-right">S/ {{ formatNumber(detalle.precio_unitario) }}</td>
                    <td class="px-4 py-3">
                      <div class="flex items-center gap-2 justify-end">
                        <button @click="decrementarRecepcion(detalle.id_detalle_solicitud)"
                          :disabled="recepcionCantidades[detalle.id_detalle_solicitud] === 0"
                          class="w-8 h-8 border border-gray-300 rounded-lg text-gray-600 hover:bg-gray-50 disabled:opacity-50">−</button>
                        <input v-model.number="recepcionCantidades[detalle.id_detalle_solicitud]" type="number"
                          :max="detalle.cantidad_pedida - (detalle.cantidad_recibida || 0)" min="0"
                          class="w-24 text-center px-2 py-1.5 border border-gray-300 rounded-lg text-xs">
                        <button
                          @click="incrementarRecepcion(detalle.id_detalle_solicitud, detalle.cantidad_pedida - (detalle.cantidad_recibida || 0))"
                          :disabled="recepcionCantidades[detalle.id_detalle_solicitud] >= (detalle.cantidad_pedida - (detalle.cantidad_recibida || 0))"
                          class="w-8 h-8 border border-gray-300 rounded-lg text-gray-600 hover:bg-gray-50 disabled:opacity-50">+</button>
                      </div>
                    </td>
                    <td class="px-4 py-3 text-right font-semibold">
                      S/ {{ formatNumber((recepcionCantidades[detalle.id_detalle_solicitud] || 0) *
                        detalle.precio_unitario) }}
                    </td>
                  </tr>
                </tbody>
                <tfoot class="bg-gray-50 border-t border-gray-200">
                  <tr>
                    <td colspan="6" class="px-4 py-3 text-right font-semibold text-gray-700">Total a recibir:</td>
                    <td class="px-4 py-3 text-right font-bold text-lg text-emerald-600">S/ {{
                      formatNumber(totalRecepcion) }}</td>
                  </tr>
                  <tr>
                    <td colspan="6" class="px-4 py-3 text-right text-xs text-gray-500">Total productos:</td>
                    <td class="px-4 py-3 text-right font-semibold">{{ totalProductosRecepcion }} unidades</td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>
        </div>

        <div class="border-t border-gray-200 px-6 py-4 bg-gray-50 flex justify-end gap-3">
          <button @click="cerrarModalRecepcion"
            class="px-4 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
          <button @click="confirmarRecepcion" :disabled="totalRecepcion === 0"
            class="px-4 py-2 text-xs font-medium text-white bg-emerald-600 rounded-lg hover:bg-emerald-700 disabled:opacity-50">Confirmar
            Recepción</button>
        </div>
      </div>
    </div>

    <!-- Modal Detalle Solicitud -->
    <div v-if="modalDetalleVisible"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="cerrarModalDetalle">
      <div class="bg-white rounded-xl w-full max-w-5xl max-h-[90vh] flex flex-col overflow-hidden">
        <div class="border-b border-gray-200 px-6 py-5 flex justify-between items-center bg-white">
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Detalle de Solicitud</h2>
            <p class="text-xs text-gray-500 font-mono">{{ solicitudDetalle?.correlativo }}</p>
          </div>
          <button @click="cerrarModalDetalle" class="text-gray-400 hover:text-gray-600 text-2xl leading-none">✕</button>
        </div>

        <div class="flex-1 overflow-y-auto p-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div class="bg-gray-50 rounded-lg p-3">
              <p class="text-xs text-gray-500">Proveedor</p>
              <p class="text-xs font-medium text-gray-900">{{ solicitudDetalle?.proveedor_nombre }}</p>
            </div>
            <div class="bg-gray-50 rounded-lg p-3">
              <p class="text-xs text-gray-500">Fecha Solicitud</p>
              <p class="text-xs font-medium text-gray-900">{{ formatFechaCompleta(solicitudDetalle?.fecha_solicitud) }}
              </p>
            </div>
            <div class="bg-gray-50 rounded-lg p-3">
              <p class="text-xs text-gray-500">Fecha Requerida</p>
              <p class="text-xs font-medium text-gray-900">{{ formatFechaShort(solicitudDetalle?.fecha_requerida) }}</p>
            </div>
            <div class="bg-gray-50 rounded-lg p-3">
              <p class="text-xs text-gray-500">Estado</p>
              <span :class="getEstadoClass(solicitudDetalle?.estado)"
                class="inline-block px-2 py-1 rounded-full text-xs font-medium">{{
                  getEstadoTexto(solicitudDetalle?.estado) }}</span>
            </div>
            <div class="bg-gray-50 rounded-lg p-3">
              <p class="text-xs text-gray-500">Comprobante</p>
              <p class="text-xs font-medium text-gray-900">{{ solicitudDetalle?.tipo_comprobante || 'Sin comprobante' }}
                {{ solicitudDetalle?.numero_comprobante }}</p>
            </div>
            <div class="bg-gray-50 rounded-lg p-3">
              <p class="text-xs text-gray-500">Forma de Pago</p>
              <p class="text-xs font-medium text-gray-900">{{ getFormaPagoTexto(solicitudDetalle?.forma_pago) }}</p>
            </div>
          </div>

          <h3 class="text-xs font-semibold text-gray-900 mb-3">Productos</h3>
          <div class="overflow-x-auto mb-6">
            <table class="w-full text-xs border border-gray-200 rounded-lg">
              <thead class="bg-gray-50">
                <tr>
                  <th class="text-left px-4 py-3 text-xs font-semibold text-gray-500">Producto</th>
                  <th class="text-right px-4 py-3 text-xs font-semibold text-gray-500">Pedido</th>
                  <th class="text-right px-4 py-3 text-xs font-semibold text-gray-500">Recibido</th>
                  <th class="text-right px-4 py-3 text-xs font-semibold text-gray-500">Pendiente</th>
                  <th class="text-right px-4 py-3 text-xs font-semibold text-gray-500">Precio Unit.</th>
                  <th class="text-right px-4 py-3 text-xs font-semibold text-gray-500">Subtotal</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="detalle in solicitudDetalle?.detalles" :key="detalle.id_detalle_solicitud">
                  <td class="px-4 py-3 font-medium text-gray-900">{{ detalle.nombre_producto }}</td>
                  <td class="px-4 py-3 text-right">{{ detalle.cantidad_pedida }}</td>
                  <td class="px-4 py-3 text-right text-emerald-600">{{ detalle.cantidad_recibida || 0 }}</td>
                  <td class="px-4 py-3 text-right text-orange-600">{{ detalle.cantidad_pedida -
                    (detalle.cantidad_recibida || 0) }}</td>
                  <td class="px-4 py-3 text-right">S/ {{ formatNumber(detalle.precio_unitario) }}</td>
                  <td class="px-4 py-3 text-right font-semibold">S/ {{ formatNumber(detalle.subtotal) }}</td>
                </tr>
              </tbody>
              <tfoot class="bg-gray-50 border-t border-gray-200">
                <tr>
                  <td colspan="5" class="px-4 py-3 text-right font-medium">Total</td>
                  <td class="px-4 py-3 text-right font-bold text-lg">S/ {{ formatNumber(solicitudDetalle?.total) }}</td>
                </tr>
              </tfoot>
            </table>
          </div>

          <div v-if="solicitudDetalle?.observaciones" class="mt-4 p-3 bg-gray-50 rounded-lg">
            <p class="text-xs text-gray-500 mb-1">Observaciones</p>
            <p class="text-xs text-gray-700">{{ solicitudDetalle.observaciones }}</p>
          </div>
        </div>

        <div class="border-t border-gray-200 px-6 py-4 bg-gray-50 flex justify-end gap-3">
          <button @click="cerrarModalDetalle"
            class="px-4 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">Cerrar</button>
          <button
            v-if="solicitudDetalle?.estado !== 4 && solicitudDetalle?.estado !== 5 && solicitudDetalle?.estado !== 6"
            @click="abrirRecepcionDesdeDetalle"
            class="px-4 py-2 text-xs font-medium text-white bg-emerald-600 rounded-lg hover:bg-emerald-700">Registrar
            Recepción</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PurchaseOrders',
  data() {
    return {
      loading: false,
      solicitudes: [],
      currentPage: 1,
      itemsPerPage: 10,
      modalSolicitudVisible: false,
      modalRecepcionVisible: false,
      modalDetalleVisible: false,
      solicitudEditando: null,
      solicitudRecepcion: null,
      solicitudDetalle: null,
      recepcionCantidades: {},
      filters: {
        numero_solicitud: '',
        proveedor: '',
        estado: '',
        fecha_desde: '',
        fecha_hasta: ''
      },
      solicitudForm: {
        proveedor_id: '',
        fecha_requerida: '',
        forma_pago: '1',
        tipo_comprobante: '',
        numero_comprobante: '',
        observaciones: '',
        productos: []
      },
      proveedores: {
        1: 'Distribuidora del Sur',
        2: 'Importaciones García',
        3: 'Corporación López'
      },
      catalogoProductos: [
        { id: 1, codigo: 'GAL-001', nombre: 'Galleta Soda', stock: 1000 },
        { id: 2, codigo: 'GAS-001', nombre: 'Coca-Cola 2.5L', stock: 500 },
        { id: 3, codigo: 'GAS-002', nombre: 'Inca Kola 3L', stock: 450 },
        { id: 4, codigo: 'ARR-001', nombre: 'Arroz Costeño 1kg', stock: 2000 },
        { id: 5, codigo: 'GAL-002', nombre: 'Galleta Ritz', stock: 600 },
        { id: 6, codigo: 'PROD-001', nombre: 'Laptop HP 15" - 8GB RAM', stock: 25 },
        { id: 7, codigo: 'PROD-002', nombre: 'Mouse Logitech M185', stock: 150 },
        { id: 8, codigo: 'PROD-003', nombre: 'Teclado USB Genius', stock: 80 },
        { id: 9, codigo: 'PROD-004', nombre: 'Monitor LG 24"', stock: 45 },
        { id: 10, codigo: 'PROD-005', nombre: 'Disco SSD 480GB', stock: 60 }
      ]
    }
  },
  computed: {
    solicitudesFiltradas() {
      let filtered = [...this.solicitudes]
      if (this.filters.numero_solicitud) filtered = filtered.filter(s => s.correlativo.toLowerCase().includes(this.filters.numero_solicitud.toLowerCase()))
      if (this.filters.proveedor) filtered = filtered.filter(s => s.proveedor_id == this.filters.proveedor)
      if (this.filters.estado) filtered = filtered.filter(s => s.estado == this.filters.estado)
      if (this.filters.fecha_desde) filtered = filtered.filter(s => s.fecha_solicitud >= this.filters.fecha_desde)
      if (this.filters.fecha_hasta) filtered = filtered.filter(s => s.fecha_solicitud <= this.filters.fecha_hasta + 'T23:59:59')
      return filtered.sort((a, b) => new Date(b.fecha_solicitud) - new Date(a.fecha_solicitud))
    },
    solicitudesPaginadas() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      return this.solicitudesFiltradas.slice(start, start + this.itemsPerPage)
    },
    totalPages() { return Math.ceil(this.solicitudesFiltradas.length / this.itemsPerPage) },
    totalInvertido() { return this.solicitudes.reduce((sum, s) => sum + (s.total || 0), 0) },
    totalPendientes() { return this.solicitudes.filter(s => s.estado === 1 || s.estado === 2).length },
    totalRecepciónParcial() { return this.solicitudes.filter(s => s.estado === 3).length },
    totalCompletadas() { return this.solicitudes.filter(s => s.estado === 4).length },
    filtrosActivos() { return this.filters.numero_solicitud || this.filters.proveedor || this.filters.estado || this.filters.fecha_desde || this.filters.fecha_hasta },
    subtotalSolicitud() { return this.solicitudForm.productos.reduce((sum, p) => sum + (p.subtotal || 0), 0) },
    totalRecepcion() {
      if (!this.solicitudRecepcion) return 0
      let total = 0
      for (const detalle of this.solicitudRecepcion.detalles) {
        total += (this.recepcionCantidades[detalle.id_detalle_solicitud] || 0) * detalle.precio_unitario
      }
      return total
    },
    totalProductosRecepcion() {
      let total = 0
      for (const detalle of this.solicitudRecepcion?.detalles || []) {
        total += this.recepcionCantidades[detalle.id_detalle_solicitud] || 0
      }
      return total
    }
  },
  mounted() { this.cargarDatosSimulados() },
  methods: {
    cargarDatosSimulados() {
      this.solicitudes = [
        { id_solicitud: 1, correlativo: 'PED-202600001', proveedor_id: 1, proveedor_nombre: 'Distribuidora del Sur', fecha_solicitud: '2026-06-01T10:30:00', fecha_requerida: '2026-06-10', estado: 4, forma_pago: 1, tipo_comprobante: 'Factura', numero_comprobante: 'F001-00012345', total: 12500.00, total_recibido: 12500.00, observaciones: 'Entrega a tiempo', detalles: [{ id_detalle_solicitud: 1, nombre_producto: 'Laptop HP 15" - 8GB RAM', cantidad_pedida: 10, cantidad_recibida: 10, precio_unitario: 1250.00, subtotal: 12500.00 }], recepciones: [] },
        { id_solicitud: 2, correlativo: 'PED-202600002', proveedor_id: 2, proveedor_nombre: 'Importaciones García', fecha_solicitud: '2026-06-03T09:15:00', fecha_requerida: '2026-06-15', estado: 3, forma_pago: 2, tipo_comprobante: 'Factura', numero_comprobante: 'B001-0009876', total: 3450.00, total_recibido: 2300.00, observaciones: 'Pendiente 5 monitores', detalles: [{ id_detalle_solicitud: 2, nombre_producto: 'Monitor LG 24"', cantidad_pedida: 15, cantidad_recibida: 10, precio_unitario: 230.00, subtotal: 3450.00 }], recepciones: [] },
        { id_solicitud: 3, correlativo: 'PED-202600003', proveedor_id: 3, proveedor_nombre: 'Corporación López', fecha_solicitud: '2026-06-05T14:45:00', fecha_requerida: '2026-06-20', estado: 1, forma_pago: 1, tipo_comprobante: 'Boleta', numero_comprobante: '', total: 875.50, total_recibido: 0, observaciones: 'Productos periféricos', detalles: [{ id_detalle_solicitud: 3, nombre_producto: 'Mouse Logitech M185', cantidad_pedida: 25, cantidad_recibida: 0, precio_unitario: 18.50, subtotal: 462.50 }, { id_detalle_solicitud: 4, nombre_producto: 'Teclado USB Genius', cantidad_pedida: 15, cantidad_recibida: 0, precio_unitario: 27.50, subtotal: 412.50 }], recepciones: [] },
        { id_solicitud: 4, correlativo: 'PED-202600004', proveedor_id: 1, proveedor_nombre: 'Distribuidora del Sur', fecha_solicitud: '2026-06-08T08:00:00', fecha_requerida: '2026-06-25', estado: 2, forma_pago: 1, tipo_comprobante: 'Factura', numero_comprobante: 'F001-00012400', total: 12400.00, total_recibido: 0, observaciones: 'Envío confirmado', detalles: [{ id_detalle_solicitud: 5, nombre_producto: 'Disco SSD 480GB', cantidad_pedida: 40, cantidad_recibida: 0, precio_unitario: 310.00, subtotal: 12400.00 }], recepciones: [] }
      ]
    },

    buscarProductos(producto, textoBusqueda) {
      if (!textoBusqueda || textoBusqueda.length < 2) {
        producto.resultados = []
        producto.mostrarResultados = false
        return
      }
      setTimeout(() => {
        const busquedaLower = textoBusqueda.toLowerCase()
        producto.resultados = this.catalogoProductos.filter(p => p.nombre.toLowerCase().includes(busquedaLower) || p.codigo.toLowerCase().includes(busquedaLower)).slice(0, 10)
        producto.mostrarResultados = true
      }, 300)
    },

    mostrarResultados(producto) {
      if (producto.buscador && producto.buscador.length >= 2 && producto.resultados && producto.resultados.length > 0) {
        producto.mostrarResultados = true
      }
    },

    ocultarResultados(producto) {
      setTimeout(() => { producto.mostrarResultados = false }, 300)
    },

    seleccionarProducto(producto, productoSeleccionado) {
      producto.id_producto = productoSeleccionado.id
      producto.buscador = productoSeleccionado.nombre
      producto.cantidad_paquetes = 0
      producto.unidades_por_paquete = 1
      producto.precio_paquete = 0
      producto.total_unidades = 0
      producto.subtotal = 0
      producto.precio_venta_unidad = 0
      producto.precio_venta_editable = 0
      producto.ganancia_total = 0
      producto.ganancia_porcentaje = 0
      producto.mostrarResultados = false
      producto.resultados = []
    },

    calcularProducto(producto) {
      const paquetes = Number(producto.cantidad_paquetes) || 0
      const unidadesPorPaquete = Number(producto.unidades_por_paquete) || 1
      const precioPaquete = Number(producto.precio_paquete) || 0

      // Guardar el precio editable anterior para comparar
      const precioEditableAnterior = producto.precio_venta_editable
      const costoPorUnidadAnterior = producto.precio_venta_unidad

      // 1. Calcular total de unidades
      producto.total_unidades = paquetes * unidadesPorPaquete

      // 2. Calcular subtotal
      producto.subtotal = paquetes * precioPaquete

      // 3. Calcular costo por unidad
      if (producto.total_unidades > 0 && producto.subtotal > 0) {
        const costoPorUnidad = producto.subtotal / producto.total_unidades
        producto.precio_venta_unidad = Math.round(costoPorUnidad * 100) / 100

        // Calcular precio sugerido (30% de ganancia)
        const margenGanancia = 1.30
        const precioVentaSugerido = Math.round((costoPorUnidad * margenGanancia) * 100) / 100
        producto.precio_sugerido = precioVentaSugerido

        // 🔥 SOLUCIÓN: Si el costo por unidad cambió, actualizar el precio editable
        // pero SOLO si el usuario no ha hecho una edición manual significativa
        const costoCambioSignificativo = Math.abs(costoPorUnidad - costoPorUnidadAnterior) > 0.01

        if (costoCambioSignificativo) {
          // Si el costo cambió mucho, actualizar el precio sugerido
          producto.precio_venta_editable = precioVentaSugerido
        } else if (!producto.precio_venta_editable || producto.precio_venta_editable === 0) {
          // Si nunca tuvo precio, asignarlo
          producto.precio_venta_editable = precioVentaSugerido
        } else {
        }
      } else {
        producto.precio_venta_unidad = 0
        producto.precio_sugerido = 0
        if (!producto.precio_venta_editable) producto.precio_venta_editable = 0
      }

      // 4. Calcular la ganancia
      this.calcularGanancia(producto)
    },

    calcularGanancia(producto) {
      if (producto.total_unidades > 0 && producto.precio_venta_editable > 0) {
        const precioVenta = Number(producto.precio_venta_editable)
        const costoPorUnidad = Number(producto.precio_venta_unidad)
        if (costoPorUnidad > 0) {
          const gananciaPorUnidad = precioVenta - costoPorUnidad
          producto.ganancia_total = Math.round((gananciaPorUnidad * producto.total_unidades) * 100) / 100
          const porcentaje = ((precioVenta - costoPorUnidad) / costoPorUnidad) * 100
          producto.ganancia_porcentaje = Math.round(porcentaje * 100) / 100
        } else {
          producto.ganancia_total = 0
          producto.ganancia_porcentaje = 0
        }
      } else {
        producto.ganancia_total = 0
        producto.ganancia_porcentaje = 0
      }
    },

    aplicarFiltros() { this.currentPage = 1 },

    limpiarFiltros() {
      this.filters = { numero_solicitud: '', proveedor: '', estado: '', fecha_desde: '', fecha_hasta: '' }
      this.currentPage = 1
    },

    getProveedorNombre(id) { return this.proveedores[id] || '' },
    getEstadoTexto(estado) {
      const estados = { 1: 'Pendiente', 2: 'Pedido enviado', 3: 'Recibido parcial', 4: 'Recibido completo', 5: 'Anulada', 6: 'Cerrada' }
      return estados[estado] || 'Desconocido'
    },
    getEstadoClass(estado) {
      const classes = { 1: 'bg-gray-100 text-gray-700', 2: 'bg-blue-50 text-blue-700', 3: 'bg-orange-50 text-orange-700', 4: 'bg-emerald-50 text-emerald-700', 5: 'bg-red-50 text-red-700', 6: 'bg-gray-100 text-gray-500' }
      return classes[estado] || 'bg-gray-100 text-gray-700'
    },
    getFormaPagoTexto(forma) {
      const formas = { 1: 'Contado', 2: 'Crédito', 3: 'Mixto' }
      return formas[forma] || 'Contado'
    },
    formatFechaShort(fecha) {
      if (!fecha) return ''
      return new Date(fecha).toLocaleDateString('es-PE', { day: '2-digit', month: '2-digit', year: 'numeric' })
    },
    formatHora(fecha) {
      if (!fecha) return ''
      return new Date(fecha).toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
    },
    formatFechaCompleta(fecha) {
      if (!fecha) return ''
      return new Date(fecha).toLocaleDateString('es-PE', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
    },
    formatNumber(number) {
      if (number === undefined || number === null) return '0.00'
      return number.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    },

    abrirNuevaSolicitud() {
      this.solicitudEditando = null
      this.solicitudForm = {
        proveedor_id: '',
        fecha_requerida: new Date().toISOString().split('T')[0],
        forma_pago: '1',
        tipo_comprobante: '',
        numero_comprobante: '',
        observaciones: '',
        productos: []
      }
      this.modalSolicitudVisible = true
    },

    agregarProducto() {
      this.solicitudForm.productos.push({
        id_producto: '',
        buscador: '',
        cantidad_paquetes: 0,
        unidades_por_paquete: 1,
        precio_paquete: 0,
        total_unidades: 0,
        subtotal: 0,
        precio_venta_unidad: 0,
        precio_venta_editable: 0,
        ganancia_total: 0,
        ganancia_porcentaje: 0,
        resultados: [],
        mostrarResultados: false
      })
    },

    eliminarProducto(index) { this.solicitudForm.productos.splice(index, 1) },

    guardarSolicitud() {
      if (!this.solicitudForm.proveedor_id) { alert('Seleccione un proveedor'); return }
      if (this.solicitudForm.productos.length === 0) { alert('Agregue al menos un producto'); return }

      for (const producto of this.solicitudForm.productos) {
        if (!producto.id_producto) { alert('Debe seleccionar un producto válido para todas las filas'); return }
        if (producto.cantidad_paquetes === 0) { alert('Debe ingresar al menos 1 paquete'); return }
        if (!producto.precio_paquete || producto.precio_paquete <= 0) { alert('Debe ingresar un precio de compra válido'); return }
      }

      const nuevaSolicitud = {
        id_solicitud: Date.now(),
        correlativo: `PED-${new Date().getFullYear()}${String(this.solicitudes.length + 1).padStart(6, '0')}`,
        proveedor_id: parseInt(this.solicitudForm.proveedor_id),
        proveedor_nombre: this.getProveedorNombre(parseInt(this.solicitudForm.proveedor_id)),
        fecha_solicitud: new Date().toISOString(),
        fecha_requerida: this.solicitudForm.fecha_requerida,
        estado: 1,
        forma_pago: parseInt(this.solicitudForm.forma_pago),
        tipo_comprobante: this.solicitudForm.tipo_comprobante,
        numero_comprobante: this.solicitudForm.numero_comprobante,
        total: this.subtotalSolicitud * 1.18,
        total_recibido: 0,
        observaciones: this.solicitudForm.observaciones,
        detalles: this.solicitudForm.productos.map((p, idx) => {
          const productoEncontrado = this.catalogoProductos.find(prod => prod.id === p.id_producto)
          return {
            id_detalle_solicitud: Date.now() + idx,
            nombre_producto: productoEncontrado?.nombre || 'Producto',
            cantidad_pedida: p.total_unidades,
            cantidad_paquetes: p.cantidad_paquetes,
            unidades_por_paquete: p.unidades_por_paquete,
            cantidad_recibida: 0,
            precio_unitario: p.precio_paquete,
            precio_venta_unidad: p.precio_venta_unidad,
            subtotal: p.subtotal
          }
        }),
        recepciones: []
      }

      this.solicitudes.push(nuevaSolicitud)
      this.cerrarModalSolicitud()
      alert('Solicitud creada exitosamente')
    },

    verDetalle(solicitud) {
      this.solicitudDetalle = solicitud
      this.modalDetalleVisible = true
    },

    abrirRecepcion(solicitud) {
      this.solicitudRecepcion = JSON.parse(JSON.stringify(solicitud))
      this.recepcionCantidades = {}
      for (const detalle of this.solicitudRecepcion.detalles) {
        const pendiente = (detalle.cantidad_pedida || 0) - (detalle.cantidad_recibida || 0)
        this.recepcionCantidades[detalle.id_detalle_solicitud] = pendiente > 0 ? pendiente : 0
      }
      this.modalRecepcionVisible = true
    },

    abrirRecepcionDesdeDetalle() {
      this.modalDetalleVisible = false
      this.abrirRecepcion(this.solicitudDetalle)
    },

    incrementarRecepcion(detalleId, max) {
      const current = this.recepcionCantidades[detalleId] || 0
      if (current < max) this.recepcionCantidades[detalleId] = current + 1
    },

    decrementarRecepcion(detalleId) {
      const current = this.recepcionCantidades[detalleId] || 0
      if (current > 0) this.recepcionCantidades[detalleId] = current - 1
    },

    confirmarRecepcion() {
      const solicitudOriginal = this.solicitudes.find(s => s.id_solicitud === this.solicitudRecepcion.id_solicitud)
      let totalRecibidoAhora = 0
      let productosRecibidos = []

      for (const detalle of solicitudOriginal.detalles) {
        const cantidadRecibir = this.recepcionCantidades[detalle.id_detalle_solicitud] || 0
        if (cantidadRecibir > 0) {
          const monto = cantidadRecibir * detalle.precio_unitario
          totalRecibidoAhora += monto
          productosRecibidos.push(`${detalle.nombre_producto} (${cantidadRecibir} und)`)
          detalle.cantidad_recibida = (detalle.cantidad_recibida || 0) + cantidadRecibir
        }
      }

      if (totalRecibidoAhora === 0) { alert('No hay productos para recibir'); return }

      solicitudOriginal.total_recibido = (solicitudOriginal.total_recibido || 0) + totalRecibidoAhora
      if (!solicitudOriginal.recepciones) solicitudOriginal.recepciones = []
      solicitudOriginal.recepciones.push({
        fecha: new Date().toISOString(),
        monto: totalRecibidoAhora,
        productos: productosRecibidos.join(', '),
        usuario: 'Admin'
      })

      const totalPedido = solicitudOriginal.total
      const totalRecibido = solicitudOriginal.total_recibido
      if (totalRecibido >= totalPedido) solicitudOriginal.estado = 4
      else if (totalRecibido > 0) solicitudOriginal.estado = 3

      this.cerrarModalRecepcion()
      alert(`Recepción confirmada por S/ ${this.formatNumber(totalRecibidoAhora)}`)
    },

    cerrarModalSolicitud() {
      this.modalSolicitudVisible = false
      this.solicitudEditando = null
    },

    cerrarModalRecepcion() {
      this.modalRecepcionVisible = false
      this.solicitudRecepcion = null
      this.recepcionCantidades = {}
    },

    cerrarModalDetalle() {
      this.modalDetalleVisible = false
      this.solicitudDetalle = null
    }
  }
}
</script>

<style scoped>
.border-l-3 {
  border-left-width: 3px;
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  opacity: 0.5;
}

table input {
  transition: all 0.2s ease;
}

table input:focus {
  border-color: #6b7280;
  box-shadow: 0 0 0 2px rgba(107, 114, 128, 0.1);
}

.overflow-y-auto {
  scroll-behavior: smooth;
}
</style>