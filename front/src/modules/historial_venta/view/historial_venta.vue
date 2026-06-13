<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 px-8 py-6">
      <div class="flex justify-between items-start">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center flex-shrink-0">
            <span class="text-white text-xs font-bold">H</span>
          </div>
          <div>
            <h1 class="text-base sm:text-xl font-semibold text-gray-800 tracking-tight">Historial de Ventas</h1>
            <p class="text-xs text-gray-500 hidden sm:block">Administración de transacciones</p>
          </div>
        </div>
        <!-- <div class="flex gap-3">
          <button class="px-5 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            Exportar
          </button>
        </div> -->
      </div>
    </header>

    <!-- Main Content -->
    <main class="px-8 py-6">
      <!-- KPI Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg border border-gray-200 p-5">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-xs font-medium text-gray-500 tracking-wide">Ventas Total</p>
              <p class="text-2xl font-bold text-gray-900 mt-2">S/ {{ formatNumber(totalVentas) }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg border border-gray-200 p-5">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-xs font-medium text-gray-500 tracking-wide">Devoluciones</p>
              <p class="text-2xl font-bold text-rose-600 mt-2">S/ {{ formatNumber(totalDevuelto) }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg border border-gray-200 p-5">
          <div>
            <p class="text-xs font-medium text-gray-500 tracking-wide">Saldo Final</p>
            <p class="text-2xl font-bold text-emerald-600 mt-2">S/ {{ formatNumber(totalVentas - totalDevuelto) }}</p>
          </div>
        </div>
        
        <div class="bg-white rounded-lg border border-gray-200 p-5">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-xs font-medium text-gray-500 tracking-wide">Transacciones</p>
              <p class="text-2xl font-bold text-gray-900 mt-2">{{ pagination.total }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters Panel -->
      <div class="bg-white rounded-lg border border-gray-200 mb-8">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-xs font-semibold text-gray-700 flex items-center gap-2">
            <span class="w-1 h-4 bg-gray-900 rounded-full"></span>
            Filtros de busqueda
          </h2>
        </div>
        
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            <div>
              <label class="block text-xs font-medium text-gray-500 tracking-wide mb-1">Nº de Venta</label>
              <input 
                v-model="filters.numero_venta"
                type="text"
                placeholder="V-XXXXXX"
                class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none"
              >
            </div>
            
            <div>
              <label class="block text-xs font-medium text-gray-500 tracking-wide mb-1">Criterio</label>
              <select v-model="filters.tipo_filtro" class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none bg-white">
                <option value="fecha">Fecha exacta</option>
                <option value="mes">Periodo mensual</option>
                <option value="rango">Intervalo personalizado</option>
                <option value="estado">Clasificación por estado</option>
              </select>
            </div>

            <div v-if="filters.tipo_filtro === 'fecha'" class="lg:col-span-2">
              <label class="block text-xs font-medium text-gray-500 tracking-wide mb-1">Fecha específica</label>
              <input v-model="filters.fecha" type="date" class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none">
            </div>
            
            <div v-else-if="filters.tipo_filtro === 'mes'" class="lg:col-span-2">
              <label class="block text-xs font-medium text-gray-500 tracking-wide mb-1">Seleccionar mes</label>
              <input v-model="filters.mes" type="month" class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none">
            </div>
            
            <div v-else-if="filters.tipo_filtro === 'estado'" class="lg:col-span-2">
              <label class="block text-xs font-medium text-gray-500 tracking-wide mb-1">Estado de venta</label>
              <select v-model="filters.estado" class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none bg-white">
                <option value="">Todas</option>
                <option value="1">Pagado</option>
                <option value="2">Devolución Parcial</option>
                <option value="3">Devolución Total</option>
              </select>
            </div>

            <div v-else-if="filters.tipo_filtro === 'rango'" class="lg:col-span-3">
              <label class="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Rango de fechas</label>
              <div class="flex gap-3">
                <input v-model="filters.fecha_desde" type="date" class="flex-1 px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none">
                <span class="text-gray-400 self-center">—</span>
                <input v-model="filters.fecha_hasta" type="date" class="flex-1 px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none">
              </div>
            </div>

            <div class="flex items-end">
              <button @click="aplicarFiltros" class="w-full px-4 py-2 bg-gray-900 text-white text-xs font-medium rounded-lg hover:bg-gray-800 transition-colors">
                Aplicar filtros
              </button>
            </div>
          </div>
          
          <div v-if="filtrosActivos" class="mt-4 pt-4 border-t border-gray-100 flex items-center gap-2 flex-wrap">
            <span class="text-xs text-gray-500">Filtros activos:</span>
            <span class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700">
              {{ textoFiltro }}
            </span>
            <span v-if="filters.estado" class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700">
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
        <p class="text-gray-500 mt-4">Cargando transacciones...</p>
      </div>

      <!-- Transactions Table -->
      <div v-else class="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h2 class="text-xs font-semibold text-gray-700 flex items-center gap-2">
            <span class="w-1 h-4 bg-gray-900 rounded-full"></span>
            Historial de transacciones
          </h2>
          <span class="text-xs text-gray-500">{{ pagination.total }} resultados</span>
        </div>
        
        <div class="overflow-x-auto" v-if="ventas.length > 0">
          <table class="w-full">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Nº de Venta</th>
                <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Fecha / Hora</th>
                <th class="text-right px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Importe Total</th>
                <th class="text-right px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Devoluciones</th>
                <th class="text-right px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Saldo Final</th>
                <th class="text-center px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Estado</th>
                <th class="text-center px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Métodos de Pago</th>
                <th class="text-center px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="venta in ventas" :key="venta.id_venta" class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4">
                  <div class="text-xs text-gray-900">{{ venta.correlativo_venta }}</div>
                </td>
                <td class="px-6 py-4">
                  <div class="text-xs text-gray-900">{{ formatFechaShort(venta.fecha_venta) }}</div>
                  <div class="text-xs text-gray-400">{{ formatHora(venta.fecha_venta) }}</div>
                </td>
                <td class="px-6 py-4 text-right font-bold text-xs text-gray-900">S/ {{ formatNumber(venta.total_venta) }}</td>
                <td class="px-6 py-4 text-right">
                  <span v-if="venta.devolucion_total_monto > 0" class="text-red-600 font-bold text-xs">
                    S/ {{ formatNumber(venta.devolucion_total_monto) }}
                  </span>
                  <span v-else class="font-bold text-xs text-gray-300">S/0</span>
                </td>
                <td class="px-6 py-4 text-right font-bold text-xs text-gray-900">S/ {{ formatNumber(venta.total_venta - (venta.devolucion_total_monto || 0)) }}</td>
                <td class="px-6 py-4 text-center">
                  <span :class="{
                    'bg-green-100 text-green-700': venta.estado_venta === 1, 
                    // Pagado = 1
                    // Devolucion Parcial = 2
                    // Devolucion Total
                    'bg-orange-100 text-orange-700': venta.estado_venta === 2,
                    'bg-gray-100 text-gray-600': venta.estado_venta === 3
                  }" class="inline-block px-2.5 py-1 rounded-full text-xs font-medium">
                    {{ getEstadoTexto(venta.estado_venta) }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <div class="flex gap-1 justify-center flex-wrap">
                    <!--         
                    (1, 'Efectivo'),
                    (2, 'Yape'),
                    (3, 'Tarjeta'),
                    (4, 'Transferencia'), 
                    -->
                    <span v-for="pago in venta.pagos.slice(0, 2)" :key="pago.id_pago" 
                      :class="{
                        'px-2 py-1 bg-green-100 rounded text-green-700 text-xs font-medium': pago.forma_pago === 1,
                        'px-2 py-1 bg-purple-100 rounded text-purple-700 text-xs font-medium': pago.forma_pago === 2,
                        'px-2 py-1 bg-gray-100 rounded text-gray-700 text-xs font-medium': pago.forma_pago !== 1 && pago.id_pago !== 2
                      }"
                      class="px-2 py-1 rounded text-xs font-medium">
                      {{ getFormaPagoTexto(pago.forma_pago) }}
                    </span>
                    <span v-if="venta.pagos.length > 2" class="px-2 py-1 bg-gray-200 rounded text-xs font-medium text-gray-600">
                      +{{ venta.pagos.length - 2 }}
                    </span>
                  </div>
                </td>
                <td class="px-6 py-4 text-center">
                  <div class="flex justify-center gap-2">
                    <button @click="verDetalleCompleto(venta)"
                      class="text-xs font-medium text-gray-600 hover:text-blue-600 px-3 py-1.5 rounded-md hover:bg-blue-50 transition-all">
                      <Icons.EyeIcon class="w-4 h-4 inline mr-1" />
                      Ver
                    </button>
                    <!-- 1 = Pagado : 2 = Devolucion parcial : 3 = Devolucion total -->
                    <button @click="abrirDevolucion(venta)" :disabled="venta.estado_venta === 3"
                      class="text-xs font-medium text-gray-600 hover:text-red-600 px-3 py-1.5 rounded-md hover:bg-red-50 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
                      <Icons.ArrowUturnLeftIcon class="w-4 h-4 inline mr-1" />
                      Devolver
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-else class="text-center py-16">
          <p class="text-gray-500">No se encontraron transacciones</p>
          <p class="text-xs text-gray-400 mt-1">Modifica los filtros para ampliar la búsqueda</p>
        </div>

        <!-- Paginación -->
        <div class="px-6 py-4 border-t border-gray-200 flex justify-between items-center">
          <div class="text-xs text-gray-500">
            Mostrando {{ pagination.from || 0 }} - {{ pagination.to || 0 }} de {{ pagination.total }} resultados
          </div>
          <div class="flex gap-2">
            <button 
              @click="cargarPagina(pagination.previous)" 
              :disabled="!pagination.previous"
              class="px-3 py-1 text-xs border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              Anterior
            </button>
            <span class="px-3 py-1 text-xs bg-gray-100 rounded-lg">
              Página {{ pagination.current_page }} de {{ pagination.total_pages }}
            </span>
            <button 
              @click="cargarPagina(pagination.next)" 
              :disabled="!pagination.next"
              class="px-3 py-1 text-xs border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              Siguiente
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Detail Modal -->
    <div v-if="modalDetalleVisible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="cerrarModalDetalle">
      <div class="bg-white rounded-xl w-full max-w-6xl max-h-[90vh] flex flex-col overflow-hidden">
        <div class="border-b border-gray-200 px-6 py-5 flex justify-between items-center bg-white">
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Información de Transacción</h2>
            <p class="text-xs text-gray-500">{{ ventaDetalle?.correlativo_venta }}</p>
          </div>
          <button @click="cerrarModalDetalle" class="text-gray-400 hover:text-gray-600 text-2xl leading-none">✕</button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6">
          <!-- Summary Grid -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-gray-50 rounded-lg p-4">
              <p class="text-xs text-gray-500 uppercase tracking-wide">Fecha de emisión</p>
              <p class="text-xs font-medium text-gray-900 mt-1">{{ formatFechaCompleta(ventaDetalle?.fecha_venta) }}</p>
            </div>
            <div class="bg-gray-50 rounded-lg p-4">
              <p class="text-xs text-gray-500 uppercase tracking-wide">Estado actual</p>
              <div class="mt-1">
                <span :class="{
                  'bg-green-50 text-green-700': ventaDetalle?.estado_venta === 1,
                  'bg-orange-50 text-orange-700': ventaDetalle?.estado_venta === 2,
                  'bg-gray-100 text-gray-600': ventaDetalle?.estado_venta === 3
                }" class="inline-block px-2.5 py-1 rounded-full text-xs font-medium">
                  {{ getEstadoTexto(ventaDetalle?.estado_venta) }}
                </span>
              </div>
            </div>
            <div class="bg-gray-50 rounded-lg p-4">
              <p class="text-xs text-gray-500 uppercase tracking-wide">Total Venta</p>
              <p class="text-xl font-bold text-gray-900 mt-1">S/ {{ formatNumber(ventaDetalle?.total_venta) }}</p>
            </div>
            <div class="bg-gray-50 rounded-lg p-4">
              <p class="text-xs text-gray-500 uppercase tracking-wide">Total Devolución</p>
              <p class="text-xl font-bold text-red-600 mt-1">S/ {{ formatNumber(ventaDetalle?.devolucion_total_monto) }}</p>
            </div>
          </div>
          
          <!-- Payment Methods -->
          <div class="mb-6">
            <h3 class="text-xs font-semibold text-gray-900 mb-3 border-l-3 border-gray-900 pl-3">Métodos de pago utilizados</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              <div v-for="pago in ventaDetalle?.pagos" :key="pago.id_pago" class="bg-gray-50 rounded-lg p-3 border border-gray-200">
                <p class="font-medium text-gray-900 text-xs">{{ getFormaPagoTexto(pago.forma_pago) }}</p>
                <p class="text-lg font-bold text-gray-900 mt-1">S/ {{ formatNumber(pago.efectivo_recibido || pago.monto_pagar) }}</p>
                <div v-if="pago.forma_pago === 1 && pago.efectivo_recibido" class="mt-2 pt-2 border-t border-gray-200 text-xs text-gray-500">
                  <!-- <p>Recibido: S/ {{ formatNumber(pago.efectivo_recibido) }}</p> -->
                  <p class="text-green-600">Vuelto: S/ {{ formatNumber(pago.efectivo_vuelto) }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Products Table -->
          <div class="mb-6">
            <h3 class="text-xs font-semibold text-gray-900 mb-3 border-l-3 border-gray-900 pl-3">Productos</h3>
            <div class="overflow-x-auto">
              <table class="w-full text-xs">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="text-left px-3 py-2 text-xs font-semibold text-gray-500">Producto</th>
                    <th class="text-left px-3 py-2 text-xs font-semibold text-gray-500">Código barra</th>
                    <th class="text-right px-3 py-2 text-xs font-semibold text-gray-500">Cantidad</th>
                    <th class="text-right px-3 py-2 text-xs font-semibold text-gray-500">Precio Unit.</th>
                    <th class="text-right px-3 py-2 text-xs font-semibold text-gray-500">Subtotal</th>
                    <th class="text-center px-3 py-2 text-xs font-semibold text-gray-500">Estado</th>
                    <th class="text-right px-3 py-2 text-xs font-semibold text-gray-500">Cantidad Devuelta</th>
                    <th class="text-right px-3 py-2 text-xs font-semibold text-gray-500">Devolución</th>
                    <th class="text-right px-3 py-2 text-xs font-semibold text-gray-500">Total</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="detalle in ventaDetalle?.detalles" :key="detalle.id_detalle">
                    <td class="px-3 py-3 font-medium text-gray-900">{{ detalle.descripcion_producto }}</td>
                    <td class="px-3 py-3 font-medium text-gray-500 text-xs">{{ detalle.codigo_barra }}</td>
                    <td class="px-3 py-3 text-right">{{ detalle.cantidad_venta }}</td>
                    <td class="px-3 py-3 text-right">S/ {{ formatNumber(detalle.precio_venta) }}</td>
                    <td class="px-3 py-3 text-right">S/ {{ formatNumber(detalle.sub_total_venta) }}</td>
                    <td class="px-3 py-3 text-center">
                      <span :class="{
                        'bg-green-50 text-green-700': detalle.estado_venta === 1,
                        'bg-orange-50 text-orange-700': detalle.estado_venta === 2,
                        'bg-gray-100 text-gray-600': detalle.estado_venta === 3
                      }" class="inline-block px-2 py-0.5 rounded-full text-xs font-medium">
                        {{ getEstadoTexto(detalle.estado_venta) }}
                      </span>
                    </td>
                    <td class="px-3 py-3 text-right">{{ detalle.devolucion_cantidad }}</td>
                    <td class="px-3 py-3 text-right">
                      <div v-if="detalle.devolucion_cantidad > 0">
                        <span class="text-gray-700">{{ detalle.devolucion_cantidad }} und.</span>
                        <div class="text-xs text-gray-400">S/ {{ formatNumber(detalle.devolucion_monto) }}</div>
                      </div>
                      <span v-else class="font-bold text-xs text-gray-600">S/0</span>
                    </td>
                    <td class="px-3 py-3 text-right font-semibold text-gray-900">S/ {{ formatNumber(detalle.sub_total_venta - detalle.devolucion_monto) }}</td>
                  </tr>
                </tbody>
                <tfoot class="bg-gray-50">
                  <tr>
                    <td colspan="7" class="px-3 py-3 text-right font-medium text-gray-700">Suma total</td>
                    <td colspan="2" class="px-3 py-3 text-right font-bold text-lg text-gray-900">
                      S/ {{ formatNumber((ventaDetalle?.total_venta || 0) - (ventaDetalle?.devolucion_total_monto || 0)) }}
                    </td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>
          
          <!-- Return History -->
          <div v-if="ventaDetalle?.devolucion_historial?.length > 0">
            <h3 class="text-xs font-semibold text-gray-900 mb-3 border-l-3 border-gray-900 pl-3">Historial de devoluciones</h3>
            <div class="space-y-2">
              <div v-for="(historial, idx) in ventaDetalle.devolucion_historial" :key="idx" class="bg-gray-50 rounded-lg p-3 flex justify-between items-center">
                <div>
                  <p class="text-xs font-medium text-gray-900">{{ historial.descripcion }}</p>
                  <p class="text-xs text-gray-500 mt-0.5">{{ formatFechaCompleta(historial.fecha) }}</p>
                </div>
                <div class="text-right">
                  <p class="text-base font-bold text-gray-900">S/ {{ formatNumber(historial.monto) }}</p>
                  <p class="text-xs text-gray-500">Usuario: {{ historial.usuario }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="border-t border-gray-200 px-6 py-4 bg-gray-50 flex justify-end gap-3">
          <button @click="cerrarModalDetalle" class="px-4 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            Cerrar
          </button>
          <button @click="abrirDevolucionDesdeDetalle" :disabled="ventaDetalle?.estado_venta === 3" class="px-4 py-2 text-xs font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed">
            {{ ventaDetalle?.estado_venta === 2 ? 'Modificar devolución' : 'Registrar devolución' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Return Modal -->
    <div v-if="modalDevolucionVisible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="cerrarModal">
      <div class="bg-white rounded-xl w-full max-w-3xl max-h-[90vh] flex flex-col overflow-hidden">
        <div class="border-b border-gray-200 px-6 py-5 flex justify-between items-center bg-white">
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Registro de Devolución</h2>
            <p class="text-xs text-gray-500">Transacción {{ ventaSeleccionada?.correlativo_venta }}</p>
          </div>
          <button @click="cerrarModal" class="text-gray-400 hover:text-gray-600 text-2xl leading-none">✕</button>
        </div>
        
        <!-- Wizard Steps -->
        <div class="px-6 py-4 bg-gray-50 border-b border-gray-200 flex items-center">
          <div v-for="(step, index) in wizardSteps" :key="index" class="flex items-center flex-1">
            <div :class="{
              'bg-gray-900 text-white': wizardStep >= index + 1,
              'bg-gray-300 text-gray-500': wizardStep < index + 1
            }" class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold">
              {{ index + 1 }}
            </div>
            <span class="ml-2 text-xs font-medium text-gray-600">{{ step }}</span>
            <div v-if="index < wizardSteps.length - 1" :class="{
              'bg-gray-400': wizardStep > index + 1,
              'bg-gray-300': wizardStep <= index + 1
            }" class="flex-1 h-0.5 mx-3"></div>
          </div>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6">
          <!-- Step 1: Return Type -->
          <div v-if="wizardStep === 1">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button @click="tipoDevolucion = 'parcial'" 
                      :class="['p-6 text-left border-2 rounded-xl transition-all', tipoDevolucion === 'parcial' ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-300']">
                <h3 class="font-semibold text-gray-900 mb-1">Devolución parcial</h3>
                <p class="text-xs text-gray-500">Selecciona productos específicos y define cantidades a devolver</p>
              </button>
              <button @click="tipoDevolucion = 'total'"
                      :class="['p-6 text-left border-2 rounded-xl transition-all', tipoDevolucion === 'total' ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-300']">
                <h3 class="font-semibold text-gray-900 mb-1">Devolución total</h3>
                <p class="text-xs text-gray-500">Devuelve el saldo pendiente de toda la transacción</p>
              </button>
            </div>
          </div>
          
          <!-- Step 2: Product Selection -->
          <div v-if="wizardStep === 2 && tipoDevolucion === 'parcial'">
            <div class="space-y-4">
              <div v-for="detalle in ventaSeleccionada?.detalles" :key="detalle.id_detalle"
                   class="border border-gray-200 rounded-xl p-4">
                <div class="flex flex-wrap gap-4">
                  <div class="flex-1">
                    <h4 class="font-semibold text-gray-900">{{ detalle.descripcion_producto }}</h4>
                    <div class="flex gap-4 mt-2 text-xs text-gray-500">
                      <span>Código barra: {{ detalle.codigo_barra || '---'}}</span>
                      <span>Comprados: {{ detalle.cantidad_venta }}</span>
                      <span v-if="detalle.devolucion_cantidad > 0">Devueltos: {{ detalle.devolucion_cantidad }}</span>
                      <span>Disponibles: {{ detalle.cantidad_venta - (detalle.devolucion_cantidad || 0) }}</span>
                    </div>
                  </div>
                  <div class="w-64">
                    <label class="text-xs text-gray-500 block mb-2">Cantidad a devolver</label>
                    <div class="flex items-center gap-2">
                      <button @click="decrementarCantidad(detalle.id_detalle)"
                              :disabled="devolucionesParciales[detalle.id_detalle]?.cantidad === 0"
                              class="w-8 h-8 border border-gray-300 rounded-lg text-gray-600 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                        −
                      </button>
                      <input v-model.number="devolucionesParciales[detalle.id_detalle].cantidad"
                             type="number"
                             :max="detalle.cantidad_venta - (detalle.devolucion_cantidad || 0)"
                             min="0"
                             class="w-20 text-center px-2 py-1.5 border border-gray-300 rounded-lg text-xs">
                      <button @click="incrementarCantidad(detalle.id_detalle, detalle.cantidad_venta - (detalle.devolucion_cantidad || 0))"
                              :disabled="devolucionesParciales[detalle.id_detalle]?.cantidad === (detalle.cantidad_venta - (detalle.devolucion_cantidad || 0))"
                              class="w-8 h-8 border border-gray-300 rounded-lg text-gray-600 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                        +
                      </button>
                    </div>
                    <div class="mt-2 text-right">
                      <span class="text-xs text-gray-500">Monto a devolver:</span>
                      <span class="ml-2 text-xs font-semibold text-gray-900">
                        S/ {{ formatNumber((devolucionesParciales[detalle.id_detalle]?.cantidad || 0) * detalle.precio_venta) }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Step 2: Total Return -->
          <div v-if="wizardStep === 2 && tipoDevolucion === 'total'" class="text-center">
            <div class="max-w-md mx-auto">
              <!-- <div class="w-12 h-12 bg-orange-100 rounded-full mx-auto mb-4"></div> -->
              <h3 class="text-lg font-semibold text-gray-900 mb-2">Confirmar devolución total</h3>
              <p class="text-gray-600 mb-6">
                Se devolverá <strong>S/ {{ formatNumber((ventaSeleccionada?.total_venta || 0) - (ventaSeleccionada?.devolucion_total_monto || 0)) }}</strong>
              </p>
              <div class="bg-gray-50 rounded-lg p-4 text-left">
                <p class="text-xs font-semibold text-gray-700 mb-2">Productos incluidos:</p>
                <ul class="space-y-1">
                  <li v-for="detalle in ventaSeleccionada?.detalles" :key="detalle.id_detalle" class="text-xs text-gray-600">
                    • {{ detalle.descripcion_producto }} - 
                    {{ (detalle.cantidad_venta || 0) - (detalle.devolucion_cantidad || 0) }} unidades pendientes
                  </li>
                </ul>
              </div>
            </div>
          </div>
          
          <!-- Step 3: Confirmation -->
          <div v-if="wizardStep === 3">
            <div class="max-w-md mx-auto">
              <div class="bg-gray-50 rounded-xl p-5">
                <div class="flex justify-between items-center pb-3 border-b border-gray-200 mb-3">
                  <span class="font-semibold text-gray-900">Resumen de la operación</span>
                  <span class="text-xs px-2 py-1 bg-gray-200 rounded-full">{{ tipoDevolucion === 'total' ? 'Devolución total' : 'Devolución parcial' }}</span>
                </div>
                
                <div v-if="tipoDevolucion === 'parcial'">
                  <div v-for="detalle in ventaSeleccionada?.detalles" :key="detalle.id_detalle">
                    <div v-if="devolucionesParciales[detalle.id_detalle]?.cantidad > 0" 
                         class="flex justify-between py-2 text-xs">
                      <span class="text-gray-600">{{ detalle.descripcion_producto }} ({{ devolucionesParciales[detalle.id_detalle].cantidad }} und)</span>
                      <span class="font-semibold text-gray-900">S/ {{ formatNumber(devolucionesParciales[detalle.id_detalle].cantidad * detalle.precio_venta) }}</span>
                    </div>
                  </div>
                  <div class="flex justify-between pt-3 mt-2 border-t border-gray-200 font-semibold">
                    <span>Total a devolver</span>
                    <span class="text-gray-900">S/ {{ formatNumber(totalDevolucionParcial) }}</span>
                  </div>
                </div>
                
                <div v-else>
                  <div class="flex justify-between py-2 text-xs">
                    <span class="text-gray-600">Total original</span>
                    <span class="font-semibold text-gray-900">S/ {{ formatNumber(ventaSeleccionada?.total_venta) }}</span>
                  </div>
                  <div class="flex justify-between py-2 text-xs">
                    <span class="text-gray-600">Ya devuelto anteriormente</span>
                    <span class="text-red-600">- S/ {{ formatNumber(ventaSeleccionada?.devolucion_total_monto || 0) }}</span>
                  </div>
                  <div class="flex justify-between pt-3 mt-2 border-t border-gray-200 font-semibold">
                    <span>Total a devolver ahora</span>
                    <span class="text-gray-900">S/ {{ formatNumber((ventaSeleccionada?.total_venta || 0) - (ventaSeleccionada?.devolucion_total_monto || 0)) }}</span>
                  </div>
                </div>
              </div>
              
              <div class="mt-4 p-3 bg-amber-50 rounded-lg text-center">
                <p class="text-xs text-amber-700">Esta acción quedará registrada en el historial de la transacción</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="border-t border-gray-200 px-6 py-4 bg-gray-50 flex justify-between">
          <button v-if="wizardStep > 1" class="px-4 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50" @click="wizardStep--">
            Anterior
          </button>
          <div class="flex-1"></div>
          <button v-if="wizardStep < 3" class="px-4 py-2 text-xs font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed" @click="siguientePaso" :disabled="!puedeAvanzar">
            Siguiente
          </button>
          <button v-if="wizardStep === 3" class="px-4 py-2 text-xs font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800" @click="confirmarDevolucion">
            Confirmar devolución
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { list_historial_ventas, get_historial_venta } from '../api/historial_venta'

export default {
  name: 'SalesDashboard',
  data() {
    return {
      loading: false,
      ventas: [],
      pagination: {
        current_page: 1,
        total_pages: 1,
        total: 0,
        from: 0,
        to: 0,
        previous: null,
        next: null
      },
      modalDetalleVisible: false,
      modalDevolucionVisible: false,
      ventaDetalle: null,
      ventaSeleccionada: null,
      tipoDevolucion: 'parcial',
      devolucionesParciales: {},
      wizardStep: 1,
      wizardSteps: ['Tipo', 'Productos', 'Confirmar'],
      activeDropdown: null,
      filters: {
        numero_venta: '',
        tipo_filtro: 'fecha',
        fecha: '',
        mes: '',
        fecha_desde: '',
        fecha_hasta: '',
        estado: ''
      }
    }
  },
  computed: {
    ventasFiltradas() {
      // Ya no se filtra localmente, la API se encarga
      return this.ventas
    },
    totalVentas() {
      return this.ventas.reduce((sum, venta) => sum + venta.total_venta, 0)
    },
    totalDevuelto() {
      return this.ventas.reduce((sum, venta) => sum + (venta.devolucion_total_monto || 0), 0)
    },
    filtrosActivos() {
      return this.filters.numero_venta || 
             (this.filters.tipo_filtro === 'fecha' && this.filters.fecha) ||
             (this.filters.tipo_filtro === 'mes' && this.filters.mes) ||
             (this.filters.tipo_filtro === 'rango' && this.filters.fecha_desde && this.filters.fecha_hasta) ||
             this.filters.estado
    },
    textoFiltro() {
      if (this.filters.numero_venta) return `N° Venta: ${this.filters.numero_venta}`
      if (this.filters.tipo_filtro === 'fecha' && this.filters.fecha) return `Fecha: ${this.filters.fecha}`
      if (this.filters.tipo_filtro === 'mes' && this.filters.mes) return `Mes: ${this.filters.mes}`
      if (this.filters.tipo_filtro === 'rango' && this.filters.fecha_desde && this.filters.fecha_hasta) 
        return `Del ${this.filters.fecha_desde} al ${this.filters.fecha_hasta}`
      return ''
    },
    totalDevolucionParcial() {
      let total = 0
      for (const detalleId in this.devolucionesParciales) {
        const detalle = this.ventaSeleccionada?.detalles.find(d => d.id_detalle === parseInt(detalleId))
        if (detalle && this.devolucionesParciales[detalleId].cantidad > 0) {
          total += this.devolucionesParciales[detalleId].cantidad * detalle.precio_venta
        }
      }
      return total
    },
    puedeAvanzar() {
      if (this.wizardStep === 1) return true
      if (this.wizardStep === 2) {
        if (this.tipoDevolucion === 'total') return true
        return this.totalDevolucionParcial > 0
      }
      return true
    }
  },
  mounted() {
    this.cargarVentas()
  },
  methods: {
    async cargarVentas(url = null) {
      this.loading = true
      
      try {
        const params = {}
        
        // Mapeo de filtros según tu API
        if (this.filters.numero_venta) params.search = this.filters.numero_venta
        if (this.filters.estado) params.estado = this.filters.estado
        
        if (this.filters.tipo_filtro === 'fecha' && this.filters.fecha) {
          params.fecha = this.filters.fecha
        } else if (this.filters.tipo_filtro === 'mes' && this.filters.mes) {
          params.mes = this.filters.mes
        } else if (this.filters.tipo_filtro === 'rango' && this.filters.fecha_desde && this.filters.fecha_hasta) {
          params.fecha_desde = this.filters.fecha_desde
          params.fecha_hasta = this.filters.fecha_hasta
        }
        
        const response = await list_historial_ventas(params)
        
        this.ventas = response.data.results
        this.pagination = {
          current_page: this.getPageNumberFromUrl(response.data.previous, response.data.next),
          total_pages: Math.ceil(response.data.count / 10),
          total: response.data.count,
          from: response.data.results.length > 0 ? (this.getPageNumberFromUrl(response.data.previous, response.data.next) - 1) * 10 + 1 : 0,
          to: Math.min(this.getPageNumberFromUrl(response.data.previous, response.data.next) * 10, response.data.count),
          previous: response.data.previous,
          next: response.data.next
        }
      } catch (error) {
        console.error('Error al cargar ventas:', error)
        alert('Error al cargar las ventas')
      } finally {
        this.loading = false
      }
    },
    
    getPageNumberFromUrl(previous, next) {
      if (previous) {
        const match = previous.match(/page=(\d+)/)
        if (match) return parseInt(match[1]) + 1
      }
      if (next) {
        const match = next.match(/page=(\d+)/)
        if (match) return parseInt(match[1]) - 1
      }
      return 1
    },
    
    cargarPagina(url) {
      if (url) {
        // Extraer los parámetros de la URL
        const urlParams = new URL(url)
        const params = new URLSearchParams(urlParams.search)
        
        const newParams = {}
        for (let [key, value] of params) {
          newParams[key] = value
        }
        
        // Mantener los filtros actuales
        if (this.filters.numero_venta) newParams.search = this.filters.numero_venta
        if (this.filters.estado) newParams.estado = this.filters.estado
        
        this.cargarVentasConParams(newParams)
      }
    },
    
    async cargarVentasConParams(params) {
      this.loading = true
      
      try {
        const response = await list_historial_ventas(params)
        
        this.ventas = response.data.results
        this.pagination = {
          current_page: this.getPageNumberFromUrl(response.data.previous, response.data.next),
          total_pages: Math.ceil(response.data.count / 10),
          total: response.data.count,
          from: response.data.results.length > 0 ? (this.getPageNumberFromUrl(response.data.previous, response.data.next) - 1) * 10 + 1 : 0,
          to: Math.min(this.getPageNumberFromUrl(response.data.previous, response.data.next) * 10, response.data.count),
          previous: response.data.previous,
          next: response.data.next
        }
      } catch (error) {
        console.error('Error al cargar ventas:', error)
        alert('Error al cargar las ventas')
      } finally {
        this.loading = false
      }
    },
    
    async verDetalleCompleto(venta) {
      this.activeDropdown = null
      this.loading = true
      
      try {
        const response = await get_historial_venta(venta.id_venta)
        this.ventaDetalle = response.data
        this.modalDetalleVisible = true
      } catch (error) {
        console.error('Error al cargar detalle:', error)
        alert('Error al cargar el detalle de la venta')
      } finally {
        this.loading = false
      }
    },
    
    aplicarFiltros() {
      this.cargarVentas()
    },
    
    limpiarFiltros() {
      this.filters = {
        numero_venta: '',
        tipo_filtro: 'fecha',
        fecha: '',
        mes: '',
        fecha_desde: '',
        fecha_hasta: '',
        estado: ''
      }
      this.cargarVentas()
    },
    
    toggleDropdown(id) {
      this.activeDropdown = this.activeDropdown === id ? null : id
    },
    
    getEstadoTexto(estado) {
      const estados = { 1: 'Pagado', 2: 'Devolución Parcial', 3: 'Devolución Total' }
      return estados[estado] || 'Desconocido'
    },
    
    getFormaPagoTexto(forma) {
      const formas = { 1: 'Efectivo', 2: 'Yape', 3: 'Tarjeta', 4: 'Transferencia' }
      return formas[forma] || 'Otro'
    },
    
    formatFechaShort(fecha) {
      return new Date(fecha).toLocaleDateString('es-PE', { day: '2-digit', month: '2-digit', year: 'numeric' })
    },
    
    formatHora(fecha) {
      return new Date(fecha).toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
    },
    
    formatFechaCompleta(fecha) {
      if (!fecha) return ''
      return new Date(fecha).toLocaleDateString('es-PE', {
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    formatNumber(number) {
      return number?.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',') || '0.00'
    },
    
    incrementarCantidad(detalleId, max) {
      const current = this.devolucionesParciales[detalleId]?.cantidad || 0
      if (current < max) {
        this.devolucionesParciales[detalleId].cantidad = current + 1
      }
    },
    
    decrementarCantidad(detalleId) {
      const current = this.devolucionesParciales[detalleId]?.cantidad || 0
      if (current > 0) {
        this.devolucionesParciales[detalleId].cantidad = current - 1
      }
    },
    
    async abrirDevolucion(venta) {
      this.activeDropdown = null
      this.loading = true
      
      try {
        // Cargar los detalles completos de la venta desde la API
        const response = await get_historial_venta(venta.id_venta)
        const ventaCompleta = response.data
        
        this.ventaSeleccionada = JSON.parse(JSON.stringify(ventaCompleta))
        this.tipoDevolucion = 'parcial'
        this.devolucionesParciales = {}
        this.wizardStep = 1
        
        // Inicializar devoluciones parciales para cada detalle
        if (this.ventaSeleccionada.detalles && this.ventaSeleccionada.detalles.length > 0) {
          this.ventaSeleccionada.detalles.forEach(detalle => {
            const cantidadDisponible = (detalle.cantidad_venta || 0) - (detalle.devolucion_cantidad || 0)
            this.devolucionesParciales[detalle.id_detalle] = {
              cantidad: 0,
              max: cantidadDisponible
            }
          })
        } else {
          alert('Esta venta no tiene productos para devolver')
          this.loading = false
          return
        }
        
        this.modalDevolucionVisible = true
      } catch (error) {
        console.error('Error al cargar detalles de la venta:', error)
        alert('Error al cargar los detalles de la venta')
      } finally {
        this.loading = false
      }
    },
    
    cerrarModal() {
      this.modalDevolucionVisible = false
      this.ventaSeleccionada = null
      this.devolucionesParciales = {}
      this.wizardStep = 1
    },
    
    cerrarModalDetalle() {
      this.modalDetalleVisible = false
      this.ventaDetalle = null
    },
    
    abrirDevolucionDesdeDetalle() {
      // ventaDetalle ya tiene los detalles porque viene de get_historial_venta
      const venta = this.ventaDetalle
      this.cerrarModalDetalle()
      
      this.ventaSeleccionada = JSON.parse(JSON.stringify(venta))
      this.tipoDevolucion = 'parcial'
      this.devolucionesParciales = {}
      this.wizardStep = 1
      
      if (this.ventaSeleccionada.detalles && this.ventaSeleccionada.detalles.length > 0) {
        this.ventaSeleccionada.detalles.forEach(detalle => {
          const cantidadDisponible = (detalle.cantidad_venta || 0) - (detalle.devolucion_cantidad || 0)
          this.devolucionesParciales[detalle.id_detalle] = {
            cantidad: 0,
            max: cantidadDisponible
          }
        })
      }
      
      this.modalDevolucionVisible = true
    },
    
    siguientePaso() {
      if (this.wizardStep === 2 && this.tipoDevolucion === 'parcial' && this.totalDevolucionParcial === 0) {
        alert('Selecciona al menos un producto para devolver')
        return
      }
      if (this.wizardStep < 3) {
        this.wizardStep++
      }
    },
    
    confirmarDevolucion() {
      const ventaOriginal = this.ventas.find(v => v.id_venta === this.ventaSeleccionada.id_venta)
      const fechaActual = new Date().toISOString()
      const usuario = 'Admin'
      
      if (this.tipoDevolucion === 'total') {
        const saldoPendiente = (ventaOriginal.total_venta || 0) - (ventaOriginal.devolucion_total_monto || 0)
        
        if (saldoPendiente > 0) {
          ventaOriginal.detalles.forEach(detalle => {
            const cantidadNoDevuelta = (detalle.cantidad_venta || 0) - (detalle.devolucion_cantidad || 0)
            if (cantidadNoDevuelta > 0) {
              const montoADevolver = cantidadNoDevuelta * detalle.precio_venta
              detalle.estado_venta = 3
              detalle.devolucion_cantidad = (detalle.devolucion_cantidad || 0) + cantidadNoDevuelta
              detalle.devolucion_monto = (detalle.devolucion_monto || 0) + montoADevolver
              if (!detalle.devolucion_historial) detalle.devolucion_historial = []
              detalle.devolucion_historial.push({
                fecha: fechaActual,
                monto: montoADevolver,
                usuario: usuario,
                descripcion: `Devolución total - ${detalle.descripcion_producto}`
              })
            }
          })
          
          ventaOriginal.estado_venta = 3
          ventaOriginal.devolucion_total_monto = ventaOriginal.total_venta
          if (!ventaOriginal.devolucion_historial) ventaOriginal.devolucion_historial = []
          ventaOriginal.devolucion_historial.push({
            fecha: fechaActual,
            monto: saldoPendiente,
            descripcion: 'Devolución total de la venta (saldo pendiente)',
            usuario: usuario
          })
          
          alert(`Devolución total confirmada por S/ ${this.formatNumber(saldoPendiente)}`)
        } else {
          alert('No hay saldo pendiente para devolver')
          return
        }
      } else {
        let totalDevuelto = 0
        let hayDevoluciones = false
        const detallesDevueltos = []
        
        for (const detalleId in this.devolucionesParciales) {
          const cantidad = this.devolucionesParciales[detalleId].cantidad
          if (cantidad > 0) {
            hayDevoluciones = true
            const detalleOriginal = ventaOriginal.detalles.find(d => d.id_detalle === parseInt(detalleId))
            const montoDevuelto = cantidad * detalleOriginal.precio_venta
            totalDevuelto += montoDevuelto
            
            detalleOriginal.devolucion_cantidad = (detalleOriginal.devolucion_cantidad || 0) + cantidad
            detalleOriginal.devolucion_monto = (detalleOriginal.devolucion_monto || 0) + montoDevuelto
            
            if (!detalleOriginal.devolucion_historial) detalleOriginal.devolucion_historial = []
            detalleOriginal.devolucion_historial.push({
              fecha: fechaActual,
              monto: montoDevuelto,
              usuario: usuario,
              descripcion: `Devolución de ${cantidad} unidad(es)`
            })
            
            if (detalleOriginal.devolucion_cantidad >= detalleOriginal.cantidad_venta) {
              detalleOriginal.estado_venta = 3
            } else if (detalleOriginal.devolucion_cantidad > 0) {
              detalleOriginal.estado_venta = 2
            }
            
            detallesDevueltos.push(`${detalleOriginal.descripcion_producto} (${cantidad} und)`)
          }
        }
        
        if (hayDevoluciones) {
          const allDevueltos = ventaOriginal.detalles.every(d => d.estado_venta === 3)
          const someDevueltos = ventaOriginal.detalles.some(d => d.estado_venta === 2 || d.estado_venta === 3)
          
          if (allDevueltos) {
            ventaOriginal.estado_venta = 3
          } else if (someDevueltos) {
            ventaOriginal.estado_venta = 2
          }
          
          ventaOriginal.devolucion_total_monto = (ventaOriginal.devolucion_total_monto || 0) + totalDevuelto
          
          if (!ventaOriginal.devolucion_historial) ventaOriginal.devolucion_historial = []
          ventaOriginal.devolucion_historial.push({
            fecha: fechaActual,
            monto: totalDevuelto,
            descripcion: `Devolución parcial - ${detallesDevueltos.join(', ')}`,
            usuario: usuario
          })
          
          alert(`Devolución parcial confirmada por S/ ${this.formatNumber(totalDevuelto)}`)
        } else {
          alert('No se seleccionó ningún producto para devolver')
          return
        }
      }
      
      const index = this.ventas.findIndex(v => v.id_venta === ventaOriginal.id_venta)
      if (index !== -1) {
        this.ventas[index] = ventaOriginal
      }
      
      this.cerrarModal()
    }
  }
}
</script>

<style scoped>
.border-l-3 {
  border-left-width: 3px;
}
</style>