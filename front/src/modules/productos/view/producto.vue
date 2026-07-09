<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Main Content -->
    <main class="px-4 sm:px-8 py-6">
      
      <!-- Filters Panel con botones integrados -->
      <div class="bg-white rounded-xl shadow-md border border-gray-200 mb-6 overflow-hidden">
        <div class="px-6 py-3.5 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
          <h2 class="text-xs font-semibold text-gray-700 flex items-center gap-2">
            <span class="w-1 h-4 bg-gray-800 rounded-full"></span>
            Filtro de búsqueda
          </h2>
          <div class="flex gap-3">
            <button @click="abrirModalExcel" class="px-4 py-1.5 text-xs font-semibold text-gray-700 bg-white border-2 border-gray-300 rounded-lg hover:bg-gray-100 transition-colors duration-200">
              Subir Excel
            </button>
            <button @click="openModal(null)" class="px-4 py-1.5 text-xs font-semibold text-white bg-gray-800 rounded-lg hover:bg-gray-900 transition-colors duration-200">
              Nuevo Producto
            </button>
          </div>
        </div>

        <div class="p-5">
          <!-- Fila 1: Búsqueda principal -->
          <div class="grid grid-cols-1 md:grid-cols-12 gap-4 mb-4">
            <div class="md:col-span-7 lg:col-span-8">
              <label class="block text-xs font-semibold text-gray-600 mb-1">Buscar producto</label>
              <div class="relative">
                <input v-model="filtroBusqueda" @input="onSearchInput" type="text"
                  placeholder="Buscar por nombre, código de barras o código interno..."
                  class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-200 transition-all duration-200 bg-white" />
                <div v-if="buscando" class="absolute right-3 top-1/2 transform -translate-y-1/2">
                  <svg class="animate-spin h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </div>
              </div>
            </div>

            <div class="md:col-span-3 lg:col-span-2">
              <label class="block text-xs font-semibold text-gray-600 mb-1">Estado</label>
              <select v-model="filtroEstado" @change="onFilterChange"
                class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-200 transition-all duration-200 bg-white">
                <option value="todos">Todos los estados</option>
                <option value="true">Activos</option>
                <option value="false">Inactivos</option>
              </select>
            </div>

            <div class="md:col-span-2 lg:col-span-2 flex items-end">
              <button v-if="filtroBusqueda || filtrosPrecioActivos" @click="limpiarTodosLosFiltros"
                class="w-full px-4 py-2 bg-gray-200 text-gray-700 text-sm font-semibold rounded-lg hover:bg-gray-300 transition-colors duration-200">
                Limpiar filtros
              </button>
            </div>
          </div>

          <!-- Fila 2: Filtros de precio -->
          <div class="grid grid-cols-1 md:grid-cols-12 gap-4">
            <div class="md:col-span-6">
              <div class="bg-gray-50 rounded-lg p-3 border border-gray-200 hover:border-gray-400 transition-colors duration-200">
                <label class="block text-xs font-semibold text-gray-600 mb-2 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Precio de Compra
                </label>
                <div class="flex items-center gap-3">
                  <div class="flex-1 relative">
                    <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 font-bold text-xs">S/</span>
                    <input 
                      v-model.number="filtroCostoMin" 
                      @input="aplicarFiltrosPrecio"
                      type="number" 
                      step="0.01" 
                      min="0"
                      placeholder="Mín"
                      class="w-full pl-7 pr-3 py-1.5 text-sm border-2 border-gray-300 rounded-lg focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-200 transition-all duration-200 bg-white" />
                  </div>
                  <span class="text-gray-400 text-sm font-light">—</span>
                  <div class="flex-1 relative">
                    <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 font-bold text-xs">S/</span>
                    <input 
                      v-model.number="filtroCostoMax" 
                      @input="aplicarFiltrosPrecio"
                      type="number" 
                      step="0.01" 
                      min="0"
                      placeholder="Máx"
                      class="w-full pl-7 pr-3 py-1.5 text-sm border-2 border-gray-300 rounded-lg focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-200 transition-all duration-200 bg-white" />
                  </div>
                </div>
              </div>
            </div>

            <div class="md:col-span-6">
              <div class="bg-gray-50 rounded-lg p-3 border border-gray-200 hover:border-gray-400 transition-colors duration-200">
                <label class="block text-xs font-semibold text-gray-600 mb-2 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                  Precio de Venta
                </label>
                <div class="flex items-center gap-3">
                  <div class="flex-1 relative">
                    <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 font-bold text-xs">S/</span>
                    <input 
                      v-model.number="filtroPrecioMin" 
                      @input="aplicarFiltrosPrecio"
                      type="number" 
                      step="0.01" 
                      min="0"
                      placeholder="Mín"
                      class="w-full pl-7 pr-3 py-1.5 text-sm border-2 border-gray-300 rounded-lg focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-200 transition-all duration-200 bg-white" />
                  </div>
                  <span class="text-gray-400 text-sm font-light">—</span>
                  <div class="flex-1 relative">
                    <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 font-bold text-xs">S/</span>
                    <input 
                      v-model.number="filtroPrecioMax" 
                      @input="aplicarFiltrosPrecio"
                      type="number" 
                      step="0.01" 
                      min="0"
                      placeholder="Máx"
                      class="w-full pl-7 pr-3 py-1.5 text-sm border-2 border-gray-300 rounded-lg focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-200 transition-all duration-200 bg-white" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Indicador de filtros activos -->
          <div v-if="filtrosPrecioActivos" class="mt-3 flex flex-wrap items-center gap-2">
            <span class="text-xs text-gray-500 font-medium">Filtros activos:</span>
            <span v-if="filtroCostoMin !== null && filtroCostoMin !== ''" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              Compra ≥ S/ {{ formatNumber(filtroCostoMin) }}
            </span>
            <span v-if="filtroCostoMax !== null && filtroCostoMax !== ''" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              Compra ≤ S/ {{ formatNumber(filtroCostoMax) }}
            </span>
            <span v-if="filtroPrecioMin !== null && filtroPrecioMin !== ''" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
              Venta ≥ S/ {{ formatNumber(filtroPrecioMin) }}
            </span>
            <span v-if="filtroPrecioMax !== null && filtroPrecioMax !== ''" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
              Venta ≤ S/ {{ formatNumber(filtroPrecioMax) }}
            </span>
            <button @click="resetearFiltrosPrecio" class="text-xs text-gray-400 hover:text-red-500 font-medium transition-colors duration-200 ml-1">
              × Limpiar filtros de precio
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-4 border-gray-200 border-t-gray-800"></div>
        <p class="text-sm font-medium text-gray-500 mt-4">Cargando productos...</p>
      </div>

      <!-- Products Table -->
      <div v-else class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
        <div class="px-6 py-3.5 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
          <h2 class="text-xs font-semibold text-gray-700 flex items-center gap-2">
            <span class="w-1 h-4 bg-gray-800 rounded-full"></span>
            Catálogo de productos
          </h2>
          <span class="text-xs text-gray-500">{{ pagination?.total || productos.length }} resultados</span>
        </div>

        <div class="overflow-x-auto" v-if="productos.length > 0">
          <table class="min-w-[920px] w-full text-sm">
            <thead class="bg-gray-100 sticky top-0 z-10 border-b-2 border-gray-200">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Código Sistema</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Producto</th>
                <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">Cantidad</th>
                <th class="px-4 py-3 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">P.Compra</th>
                <th class="px-4 py-3 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">P.Venta</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Código de Barra</th>
                <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">Estado</th>
                <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="producto in productos" :key="producto.id" class="hover:bg-gray-50 transition-colors duration-150">
                <td class="px-4 py-3.5">
                  <code class="text-xs bg-gray-200 px-2 py-1 rounded text-gray-800 font-semibold">{{ producto.codigo_interno || "Sin código" }}</code>
                </td>
                <td class="px-4 py-3.5">
                  <div class="text-sm font-semibold text-gray-800">{{ producto.nombre_producto }}</div>
                </td>
                <td class="px-4 py-3.5 text-center">
                  <span :class="[
                    'text-xs font-semibold px-2.5 py-0.5 rounded-full',
                    producto.cantidad_producto <= 5 ? 'bg-amber-100 text-amber-700' : 'bg-gray-200 text-gray-700'
                  ]">
                    {{ producto.cantidad_producto }}
                  </span>
                </td>
                <td class="px-4 py-3.5 text-right text-sm font-medium text-gray-700 whitespace-nowrap">
                  S/ {{ formatNumber(producto.costo_producto) }}
                </td>
                <td class="px-4 py-3.5 text-right">
                  <span class="px-2.5 py-1 text-xs font-semibold bg-emerald-100 text-emerald-700 rounded-lg">
                    S/ {{ formatNumber(producto.precio_unitario) }}
                  </span>
                </td>
                <td class="px-4 py-3.5">
                  <code class="text-xs bg-gray-200 px-2 py-1 rounded font-semibold text-gray-700">{{ producto.codigo_barra || "Sin código" }}</code>
                </td>
                <td class="px-4 py-3.5 text-center">
                  <span :class="[
                    'inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold',
                    producto.estado ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'
                  ]">
                    {{ producto.estado ? "Activo" : "Inactivo" }}
                  </span>
                </td>
                <td class="px-4 py-3.5 text-center">
                  <button @click="openModal(producto)"
                    class="text-xs font-semibold text-gray-600 hover:text-blue-600 px-3 py-1.5 rounded-md hover:bg-blue-50 transition-all duration-200">
                    Editar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="text-center py-16">
          <p class="text-sm font-medium text-gray-500">No se encontraron productos</p>
          <p class="text-xs text-gray-400 mt-1">Modifica los filtros para ampliar la búsqueda</p>
        </div>

        <!-- Paginación -->
        <div v-if="pagination && pagination.total > 0" class="px-6 py-4 border-t-2 border-gray-200 flex justify-between items-center">
          <div class="text-xs font-medium text-gray-500">
            Mostrando {{ pagination.from || 0 }} - {{ pagination.to || 0 }} de {{ pagination.total }} productos
          </div>
          <div class="flex gap-2">
            <button @click="cambiarPagina(pagination.previousPage)" :disabled="!pagination.previousPage"
              class="px-3.5 py-1.5 text-xs font-semibold border-2 border-gray-300 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200">
              Anterior
            </button>
            <span class="px-3.5 py-1.5 text-xs font-semibold bg-gray-100 rounded-lg text-gray-700">
              Página {{ pagination.current_page || 1 }}
            </span>
            <button @click="cambiarPagina(pagination.nextPage)" :disabled="!pagination.nextPage"
              class="px-3.5 py-1.5 text-xs font-semibold border-2 border-gray-300 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200">
              Siguiente
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal para subir Excel -->
    <div v-if="showExcelModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="cerrarModalExcel">
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-lg border border-gray-200">
        <div class="border-b-2 border-gray-200 px-6 py-5 flex justify-between items-center bg-gray-50">
          <div>
            <h2 class="text-base font-bold text-gray-800">Subir Productos desde Excel</h2>
            <p class="text-xs text-gray-500">Selecciona un archivo Excel (.xlsx, .xls)</p>
          </div>
          <button @click="cerrarModalExcel" class="text-gray-400 hover:text-gray-600 text-2xl leading-none font-light">✕</button>
        </div>

        <div class="p-6">
          <div @dragover.prevent="dragOver = true" @dragleave.prevent="dragOver = false" @drop.prevent="handleDrop"
            :class="dragOver ? 'border-gray-600 bg-gray-100' : 'border-gray-300 bg-gray-50'"
            class="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer hover:bg-gray-100 transition-colors duration-200"
            @click="$refs.fileInput.click()">
            <input ref="fileInput" type="file" accept=".xlsx,.xls" @change="handleFileUpload" class="hidden" />
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <p class="mt-2 text-sm text-gray-600">
              Arrastra y suelta tu archivo aquí, o <span class="text-gray-800 font-semibold">haz clic para seleccionar</span>
            </p>
            <p class="mt-1 text-xs text-gray-500">Formatos: .xlsx, .xls (máx. 10MB)</p>
          </div>

          <div v-if="archivoExcel" class="mt-4 p-3 bg-gray-100 rounded-lg border border-gray-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-sm text-gray-700 font-medium">{{ archivoExcel.name }}</span>
              </div>
              <button @click="archivoExcel = null; $refs.fileInput.value = ''" class="text-gray-400 hover:text-red-500 text-xl leading-none font-light">✕</button>
            </div>
          </div>

          <div v-if="subiendoExcel" class="mt-4">
            <div class="flex justify-between text-xs text-gray-600 mb-1">
              <span class="font-medium">Subiendo y procesando...</span>
              <span class="font-bold">{{ progresoCarga }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2.5">
              <div class="bg-gray-800 h-2.5 rounded-full transition-all duration-300" :style="{ width: progresoCarga + '%' }"></div>
            </div>
          </div>

          <div v-if="resultadoExcel" class="mt-4 p-3 rounded-lg border-2" :class="resultadoExcel.tipo === 'exito' ? 'bg-emerald-50 border-emerald-200 text-emerald-800' : 'bg-red-50 border-red-200 text-red-800'">
            <div class="flex items-start gap-2">
              <svg v-if="resultadoExcel.tipo === 'exito'" class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <svg v-else class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div class="flex-1">
                <p class="text-sm font-semibold">{{ resultadoExcel.mensaje }}</p>
                <div v-if="resultadoExcel.detalles && resultadoExcel.detalles.length" class="mt-2 text-xs">
                  <p class="font-medium">Detalles:</p>
                  <ul class="list-disc list-inside">
                    <li v-for="detalle in resultadoExcel.detalles.slice(0, 5)" :key="detalle">{{ detalle }}</li>
                    <li v-if="resultadoExcel.detalles.length > 5" class="text-gray-500">... y {{ resultadoExcel.detalles.length - 5 }} más</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="border-t-2 border-gray-200 px-6 py-4 bg-gray-50 flex justify-end gap-3">
          <button @click="cerrarModalExcel" class="px-4 py-2 text-xs font-semibold text-gray-700 bg-white border-2 border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            Cancelar
          </button>
          <button @click="subirExcel" :disabled="!archivoExcel || subiendoExcel"
            class="px-4 py-2 text-xs font-semibold text-white bg-gray-800 rounded-lg hover:bg-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200">
            {{ subiendoExcel ? 'Procesando...' : 'Subir Productos' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Product Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="btnCerrarModal">
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden border border-gray-200">
        <div class="border-b-2 border-gray-200 px-6 py-5 flex justify-between items-center bg-gray-50 flex-shrink-0">
          <div>
            <h2 class="text-base font-bold text-gray-800">
              {{ selectedProducto?.id ? "Actualizar Producto" : "Crear Nuevo Producto" }}
            </h2>
            <p class="text-xs text-gray-500">{{ selectedProducto?.id ? "Modifica los datos del producto" : "Ingresa los datos del nuevo producto" }}</p>
          </div>
          <button @click="btnCerrarModal" class="text-gray-400 hover:text-gray-600 text-2xl leading-none font-light">✕</button>
        </div>

        <div class="flex-1 overflow-y-auto p-6">
          <form @submit.prevent="btnConfirmar" class="space-y-6">
            <div class="bg-gray-50 rounded-lg p-4 border-2 border-gray-200">
              <h4 class="text-xs font-semibold text-gray-700 mb-4">Información del Producto</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="md:col-span-2">
                  <label class="block text-xs font-semibold text-gray-600 mb-1">Nombre del Producto <span class="text-red-500">*</span></label>
                  <input v-model="selectedProducto.nombre_producto" type="text"
                    class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-200 transition-all duration-200 bg-white" />
                  <p v-if="errors.nombre_producto" class="text-xs text-red-500 mt-1">{{ errors.nombre_producto }}</p>
                </div>

                <div>
                  <label class="block text-xs font-semibold text-gray-600 mb-1">Cantidad <span class="text-red-500">*</span></label>
                  <input v-model.number="selectedProducto.cantidad_producto" type="number" min="0"
                    :disabled="selectedProducto?.id ? true : false"
                    :class="selectedProducto?.id ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'"
                    class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-200 transition-all duration-200" />
                  <p v-if="errors.cantidad_producto" class="text-xs text-red-500 mt-1">{{ errors.cantidad_producto }}</p>
                  <p v-if="selectedProducto?.id" class="text-xs text-amber-600 mt-1 font-medium">La cantidad no se puede modificar</p>
                </div>

                <div>
                  <label class="block text-xs font-semibold text-gray-600 mb-1">Estado</label>
                  <select v-model="selectedProducto.estado"
                    class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-200 transition-all duration-200 bg-white">
                    <option :value="true">Activo</option>
                    <option :value="false">Inactivo</option>
                  </select>
                </div>
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4 border-2 border-gray-200">
              <h4 class="text-xs font-semibold text-gray-700 mb-4">Información de Precios</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-semibold text-gray-600 mb-1">Precio Compra <span class="text-red-500">*</span></label>
                  <div class="relative">
                    <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 font-bold text-sm">S/</span>
                    <input v-model.number="selectedProducto.costo_producto" type="number" step="0.01" min="0"
                      class="w-full pl-7 pr-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-200 transition-all duration-200 bg-white" />
                  </div>
                  <p v-if="errors.costo_producto" class="text-xs text-red-500 mt-1">{{ errors.costo_producto }}</p>
                </div>

                <div>
                  <label class="block text-xs font-semibold text-gray-600 mb-1">Precio Venta <span class="text-red-500">*</span></label>
                  <div class="relative">
                    <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 font-bold text-sm">S/</span>
                    <input v-model.number="selectedProducto.precio_unitario" type="number" step="0.01" min="0"
                      class="w-full pl-7 pr-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-200 transition-all duration-200 bg-white" />
                  </div>
                  <p v-if="errors.precio_unitario" class="text-xs text-red-500 mt-1">{{ errors.precio_unitario }}</p>
                </div>
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4 border-2 border-gray-200">
              <h4 class="text-xs font-semibold text-gray-700 mb-4">Información Adicional</h4>
              <div>
                <label class="block text-xs font-semibold text-gray-600 mb-1">Código de Barra</label>
                <input v-model="selectedProducto.codigo_barra" type="text" :disabled="esCodigoBarraNoEditable"
                  :class="esCodigoBarraNoEditable ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'"
                  class="w-full px-3 py-2 text-sm border-2 border-gray-300 rounded-lg focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-200 transition-all duration-200" />
                <p class="text-xs text-gray-400 mt-1">
                  Código único para identificación del producto
                  <span v-if="esCodigoBarraNoEditable" class="text-amber-600 font-medium"> (No editable)</span>
                  <span v-if="selectedProducto?.id && !selectedProducto?.codigo_barra" class="text-blue-600 font-medium"> (Puedes asignar un código)</span>
                </p>
              </div>

              <div v-if="selectedProducto?.id" class="mt-4 pt-4 border-t-2 border-gray-200">
                <label class="block text-xs font-semibold text-gray-600 mb-1">Código Interno del Sistema</label>
                <input :value="selectedProducto.codigo_interno" type="text" disabled
                  class="w-full px-3 py-2 text-sm bg-gray-100 border-2 border-gray-300 rounded-lg cursor-not-allowed text-gray-600" />
                <p class="text-xs text-gray-400 mt-1">Código generado automáticamente por el sistema</p>
              </div>
            </div>

            <div v-if="selectedProducto.id" class="bg-gray-50 rounded-lg p-4 border-2 border-gray-200">
              <h4 class="text-xs font-semibold text-gray-700 mb-4">Auditoría</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-500 font-medium">Fecha de creación:</span>
                  <span class="ml-2 text-gray-700 font-semibold">{{ formatDate(selectedProducto.fecha_creacion) }}</span>
                </div>
                <div>
                  <span class="text-gray-500 font-medium">Última actualización:</span>
                  <span class="ml-2 text-gray-700 font-semibold">{{ formatDate(selectedProducto.fecha_actualizacion) }}</span>
                </div>
              </div>
            </div>
          </form>
        </div>

        <div class="border-t-2 border-gray-200 px-6 py-4 bg-gray-50 flex justify-end gap-3 flex-shrink-0">
          <button @click="btnCerrarModal" class="px-4 py-2 text-xs font-semibold text-gray-700 bg-white border-2 border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            Cancelar
          </button>
          <button @click="btnConfirmar" :disabled="guardando"
            class="px-4 py-2 text-xs font-semibold text-white bg-gray-800 rounded-lg hover:bg-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200">
            {{ guardando ? 'Guardando...' : (selectedProducto?.id ? "Actualizar" : "Crear") }}
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="showDeleteModal = false">
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-md border border-gray-200">
        <div class="p-6">
          <div class="flex items-center justify-center mb-4">
            <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
          </div>
          <h3 class="text-lg font-bold text-center text-gray-800 mb-2">Confirmar eliminación</h3>
          <p class="text-sm text-gray-600 text-center mb-6">
            ¿Estás seguro de que deseas eliminar el producto "{{ productoAEliminar?.nombre_producto }}"?<br>
            <span class="text-xs text-gray-400">Esta acción no se puede deshacer.</span>
          </p>
          <div class="flex gap-3">
            <button @click="showDeleteModal = false" class="flex-1 px-4 py-2 text-sm font-semibold text-gray-700 bg-white border-2 border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
              Cancelar
            </button>
            <button @click="eliminarProducto" class="flex-1 px-4 py-2 text-sm font-semibold text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors duration-200">
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  list_producto,
  create_producto,
  update_producto,
  delete_producto,
  get_producto,
  importar_productos_excel
} from '../api/producto';

export default {
  name: "ProductosFormulario",
  data() {
    return {
      productos: [],
      selectedProducto: {
        nombre_producto: "",
        cantidad_producto: 0,
        costo_producto: 0,
        precio_unitario: 0,
        codigo_barra: "",
        estado: true,
      },
      showModal: false,
      showDeleteModal: false,
      productoAEliminar: null,
      
      // Filtros existentes
      filtroBusqueda: "",
      filtroEstado: "todos",
      
      // Nuevos filtros de precio
      filtroCostoMin: null,
      filtroCostoMax: null,
      filtroPrecioMin: null,
      filtroPrecioMax: null,
      
      errors: {},
      loading: false,
      guardando: false,
      pagination: null,
      searchTimeout: null,
      buscando: false,
      showExcelModal: false,
      archivoExcel: null,
      subiendoExcel: false,
      progresoCarga: 0,
      dragOver: false,
      resultadoExcel: null,
      
      // Control de debounce para filtros de precio
      precioTimeout: null,
    };
  },
  computed: {
    esCodigoBarraNoEditable() {
      if (!this.selectedProducto?.id) return false;
      if (this.selectedProducto?.codigo_barra && this.selectedProducto.codigo_barra.trim() !== '') {
        return true;
      }
      return false;
    },
    
    filtrosPrecioActivos() {
      return (this.filtroCostoMin !== null && this.filtroCostoMin !== '') || 
             (this.filtroCostoMax !== null && this.filtroCostoMax !== '') || 
             (this.filtroPrecioMin !== null && this.filtroPrecioMin !== '') || 
             (this.filtroPrecioMax !== null && this.filtroPrecioMax !== '');
    },
  },
  mounted() {
    this.cargarProductos();
  },
  beforeDestroy() {
    if (this.searchTimeout) {
      clearTimeout(this.searchTimeout);
    }
    if (this.precioTimeout) {
      clearTimeout(this.precioTimeout);
    }
  },
  methods: {
    abrirModalExcel() {
      this.showExcelModal = true;
      this.archivoExcel = null;
      this.resultadoExcel = null;
      this.progresoCarga = 0;
      this.dragOver = false;
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = '';
      }
    },

    cerrarModalExcel() {
      this.showExcelModal = false;
      this.archivoExcel = null;
      this.resultadoExcel = null;
      this.subiendoExcel = false;
      this.progresoCarga = 0;
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.validarArchivo(file);
      }
    },

    handleDrop(event) {
      this.dragOver = false;
      const file = event.dataTransfer.files[0];
      if (file) {
        this.validarArchivo(file);
      }
    },

    validarArchivo(file) {
      const tiposPermitidos = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'];
      if (!tiposPermitidos.includes(file.type) && !file.name.match(/\.(xlsx|xls)$/)) {
        this.resultadoExcel = {
          tipo: 'error',
          mensaje: 'Formato de archivo no válido. Solo se permiten archivos Excel (.xlsx, .xls)'
        };
        return;
      }

      if (file.size > 10 * 1024 * 1024) {
        this.resultadoExcel = {
          tipo: 'error',
          mensaje: 'El archivo es demasiado grande. Máximo 10MB'
        };
        return;
      }

      this.archivoExcel = file;
      this.resultadoExcel = null;
    },

    async subirExcel() {
      if (!this.archivoExcel) return;

      this.subiendoExcel = true;
      this.progresoCarga = 0;
      this.resultadoExcel = null;

      try {
        // Simular progreso
        const interval = setInterval(() => {
          if (this.progresoCarga < 90) {
            this.progresoCarga += 10;
          }
        }, 200);

        const response = await importar_productos_excel(this.archivoExcel);

        clearInterval(interval);
        this.progresoCarga = 100;

        if (response.status === 200 || response.status === 201) {
          const data = response.data;
          this.resultadoExcel = {
            tipo: 'exito',
            mensaje: data.message || 'Productos importados exitosamente',
            detalles: data.detalles || []
          };
          await this.cargarProductos();
          setTimeout(() => {
            if (this.resultadoExcel?.tipo === 'exito') {
              this.cerrarModalExcel();
            }
          }, 3000);
        } else {
          this.resultadoExcel = {
            tipo: 'error',
            mensaje: response.data?.error || 'Error al procesar el archivo',
            detalles: response.data?.detalles || []
          };
        }
      } catch (error) {
        this.resultadoExcel = {
          tipo: 'error',
          mensaje: error.response?.data?.error || error.message || 'Error de conexión. Intente nuevamente.',
          detalles: error.response?.data?.detalles || []
        };
      } finally {
        this.subiendoExcel = false;
      }
    },

    onSearchInput() {
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
      }

      if (!this.filtroBusqueda.trim()) {
        this.cargarProductos();
        return;
      }

      this.buscando = true;

      this.searchTimeout = setTimeout(() => {
        this.cargarProductos();
      }, 500);
    },

    onFilterChange() {
      this.cargarProductos();
    },

    limpiarBusqueda() {
      this.filtroBusqueda = "";
      this.cargarProductos();
    },

    limpiarTodosLosFiltros() {
      this.filtroBusqueda = "";
      this.resetearFiltrosPrecio();
    },

    // Nuevo método para aplicar filtros de precio con debounce
    aplicarFiltrosPrecio() {
      if (this.precioTimeout) {
        clearTimeout(this.precioTimeout);
      }
      
      this.precioTimeout = setTimeout(() => {
        this.cargarProductos();
      }, 400);
    },

    // Resetear todos los filtros de precio
    resetearFiltrosPrecio() {
      this.filtroCostoMin = null;
      this.filtroCostoMax = null;
      this.filtroPrecioMin = null;
      this.filtroPrecioMax = null;
      this.cargarProductos();
    },

    async cargarProductos() {
      this.loading = true;
      this.buscando = false;

      try {
        const params = {};
        if (this.filtroBusqueda) params.search = this.filtroBusqueda;
        if (this.filtroEstado !== "todos") params.estado = this.filtroEstado;
        
        // Agregar filtros de precio
        if (this.filtroCostoMin !== null && this.filtroCostoMin !== '' && this.filtroCostoMin >= 0) {
          params.costo_min = this.filtroCostoMin;
        }
        if (this.filtroCostoMax !== null && this.filtroCostoMax !== '' && this.filtroCostoMax >= 0) {
          params.costo_max = this.filtroCostoMax;
        }
        if (this.filtroPrecioMin !== null && this.filtroPrecioMin !== '' && this.filtroPrecioMin >= 0) {
          params.precio_min = this.filtroPrecioMin;
        }
        if (this.filtroPrecioMax !== null && this.filtroPrecioMax !== '' && this.filtroPrecioMax >= 0) {
          params.precio_max = this.filtroPrecioMax;
        }

        const response = await list_producto(params);

        if (response.data && response.data.results) {
          this.productos = response.data.results || [];
          const pageMatch = response.data.next?.match(/page=(\d+)/);
          const currentPage = pageMatch ? parseInt(pageMatch[1]) - 1 : 1;

          this.pagination = {
            count: response.data.count || 0,
            next: response.data.next,
            previous: response.data.previous,
            nextPage: response.data.next,
            previousPage: response.data.previous,
            total: response.data.count || 0,
            current_page: currentPage,
            from: response.data.results.length > 0 ? (currentPage - 1) * 10 + 1 : 0,
            to: Math.min(currentPage * 10, response.data.count)
          };
        } else if (Array.isArray(response.data)) {
          this.productos = response.data;
          this.pagination = null;
        } else {
          this.productos = [];
          this.pagination = null;
        }
      } catch (error) {
        console.error("Error cargando productos:", error);
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

        if (this.filtroBusqueda) params.search = this.filtroBusqueda;
        if (this.filtroEstado !== "todos") params.estado = this.filtroEstado;
        
        // Agregar filtros de precio a la paginación
        if (this.filtroCostoMin !== null && this.filtroCostoMin !== '' && this.filtroCostoMin >= 0) {
          params.costo_min = this.filtroCostoMin;
        }
        if (this.filtroCostoMax !== null && this.filtroCostoMax !== '' && this.filtroCostoMax >= 0) {
          params.costo_max = this.filtroCostoMax;
        }
        if (this.filtroPrecioMin !== null && this.filtroPrecioMin !== '' && this.filtroPrecioMin >= 0) {
          params.precio_min = this.filtroPrecioMin;
        }
        if (this.filtroPrecioMax !== null && this.filtroPrecioMax !== '' && this.filtroPrecioMax >= 0) {
          params.precio_max = this.filtroPrecioMax;
        }

        const response = await list_producto(params);

        if (response.data && response.data.results) {
          this.productos = response.data.results || [];
          const pageMatch = response.data.next?.match(/page=(\d+)/);
          const currentPage = pageMatch ? parseInt(pageMatch[1]) - 1 : 1;

          this.pagination = {
            count: response.data.count || 0,
            next: response.data.next,
            previous: response.data.previous,
            nextPage: response.data.next,
            previousPage: response.data.previous,
            total: response.data.count || 0,
            current_page: currentPage,
            from: response.data.results.length > 0 ? (currentPage - 1) * 10 + 1 : 0,
            to: Math.min(currentPage * 10, response.data.count)
          };
        }
      } catch (error) {
        console.error("Error cambiando página:", error);
      } finally {
        this.loading = false;
      }
    },

    async openModal(producto) {
      if (producto) {
        this.guardando = true;
        try {
          const response = await get_producto(producto.id);
          this.selectedProducto = { ...response.data };
        } catch (error) {
          console.error("Error cargando producto:", error);
        } finally {
          this.guardando = false;
        }
      } else {
        this.selectedProducto = {
          nombre_producto: "",
          cantidad_producto: 0,
          costo_producto: 0,
          precio_unitario: 0,
          codigo_barra: "",
          estado: true,
        };
      }
      this.errors = {};
      this.showModal = true;
    },

    btnCerrarModal() {
      this.showModal = false;
      this.selectedProducto = null;
      this.errors = {};
    },

    validarFormulario() {
      this.errors = {};

      if (!this.selectedProducto.nombre_producto || this.selectedProducto.nombre_producto.trim() === "") {
        this.errors.nombre_producto = "El nombre del producto es requerido";
      } else if (this.selectedProducto.nombre_producto.length > 250) {
        this.errors.nombre_producto = "El nombre no puede exceder los 250 caracteres";
      }

      if (!this.selectedProducto.id) {
        if (this.selectedProducto.cantidad_producto < 0) {
          this.errors.cantidad_producto = "La cantidad no puede ser negativa";
        }
      }

      if (this.selectedProducto.costo_producto < 0) {
        this.errors.costo_producto = "El costo no puede ser negativo";
      }

      if (this.selectedProducto.precio_unitario < 0) {
        this.errors.precio_unitario = "El precio unitario no puede ser negativo";
      }

      return Object.keys(this.errors).length === 0;
    },

    async btnConfirmar() {
      if (!this.validarFormulario()) {
        return;
      }

      this.guardando = true;
      try {
        if (this.selectedProducto.id) {
          const productoParaActualizar = { ...this.selectedProducto };
          delete productoParaActualizar.cantidad_producto;
          delete productoParaActualizar.codigo_barra;
          await update_producto(this.selectedProducto.id, productoParaActualizar);
        } else {
          await create_producto(this.selectedProducto);
        }
        await this.cargarProductos();
        this.btnCerrarModal();
      } catch (error) {
        console.error("Error guardando producto:", error);
        if (error.response?.data?.detalles) {
          this.errors = error.response.data.detalles;
        }
      } finally {
        this.guardando = false;
      }
    },

    confirmDelete(producto) {
      this.productoAEliminar = producto;
      this.showDeleteModal = true;
    },

    async eliminarProducto() {
      if (this.productoAEliminar) {
        try {
          await delete_producto(this.productoAEliminar.id);
          await this.cargarProductos();
        } catch (error) {
          console.error("Error eliminando producto:", error);
        } finally {
          this.showDeleteModal = false;
          this.productoAEliminar = null;
        }
      }
    },

    formatNumber(value) {
      if (value === null || value === undefined || value === '') return "0.00";
      const num = parseFloat(value);
      if (isNaN(num)) return "0.00";
      return num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },

    formatDate(dateString) {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      return date.toLocaleDateString('es-PE', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    },
  },
};
</script>