<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 px-8 py-6">
      <div class="flex justify-between items-start">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center flex-shrink-0">
            <span class="text-white text-sm font-bold">P</span>
          </div>
          <div>
            <h1 class="text-base sm:text-xl font-semibold text-gray-800 tracking-tight">Productos</h1>
            <p class="text-xs text-gray-500 hidden sm:block">Administración del inventario de productos</p>
          </div>
        </div>
        <div class="flex gap-3">
          <button @click="abrirModalExcel"
            class="px-5 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            Subir Excel
          </button>
          <button @click="openModal(null)"
            class="px-5 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 transition-colors">
            Nuevo Producto
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="px-8 py-6">
      <!-- Filters Panel -->
      <div class="bg-white rounded-lg border border-gray-200 mb-8">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-sm font-semibold text-gray-700 flex items-center gap-2">
            <span class="w-1 h-4 bg-gray-900 rounded-full"></span>
            Filtro de busqueda
          </h2>
        </div>

        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            <div class="lg:col-span-3">
              <label class="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Buscar
                producto</label>
              <div class="relative">
                <input v-model="filtroBusqueda" @input="onSearchInput" type="text"
                  placeholder="Buscar por nombre o código de barras..."
                  class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none" />
                <div v-if="buscando" class="absolute right-3 top-1/2 transform -translate-y-1/2">
                  <svg class="animate-spin h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                    </path>
                  </svg>
                </div>
              </div>
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Estado</label>
              <select v-model="filtroEstado" @change="onFilterChange"
                class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none bg-white">
                <option value="todos">Todos los estados</option>
                <option value="true">Activos</option>
                <option value="false">Inactivos</option>
              </select>
            </div>

            <div class="flex items-end">
              <button v-if="filtroBusqueda" @click="limpiarBusqueda"
                class="w-full px-4 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-200 transition-colors">
                Limpiar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
        <p class="text-gray-500 mt-4">Cargando productos...</p>
      </div>

      <!-- Products Table -->
      <div v-else class="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <h2 class="text-sm font-semibold text-gray-700 flex items-center gap-2">
            <span class="w-1 h-4 bg-gray-900 rounded-full"></span>
            Catálogo de productos
          </h2>
          <span class="text-xs text-gray-500">{{ pagination?.total || productos.length }} resultados</span>
        </div>

        <div class="overflow-x-auto" v-if="productos.length > 0">
          <table class="w-full">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Código
                  Sistema</th>
                <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Producto
                </th>
                <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Cantidad
                </th>
                <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">P.Compra
                </th>
                <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">P.Venta
                </th>
                <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Código de
                  Barra</th>
                <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Estado</th>
                <th class="text-center px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Acciones
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="producto in productos" :key="producto.id" class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4">
                  <code
                    class="text-xs bg-gray-100 px-2 py-1 rounded">{{ producto.codigo_interno || "Sin código" }}</code>
                </td>
                <td class="px-6 py-4">
                  <div class="text-sm font-semibold text-gray-900">{{ producto.nombre_producto }}</div>
                </td>
                <td class="px-6 py-4">
                  <span class="text-sm font-medium text-gray-900">{{ producto.cantidad_producto }}</span>
                </td>
                <td class="px-6 py-4">
                  <span class="text-sm text-gray-900">S/ {{ formatNumber(producto.costo_producto) }}</span>
                </td>
                <td class="px-6 py-4">
                  <span class="text-sm font-semibold text-green-600">S/ {{ formatNumber(producto.precio_unitario)
                    }}</span>
                </td>
                <td class="px-6 py-4">
                  <code class="text-xs bg-gray-100 px-2 py-1 rounded">{{ producto.codigo_barra || "Sin código" }}</code>
                </td>
                <td class="px-6 py-4">
                  <span :class="producto.estado ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-600'"
                    class="inline-block px-2.5 py-1 rounded-full text-xs font-medium">
                    {{ producto.estado ? "Activo" : "Inactivo" }}
                  </span>
                </td>
                <td class="px-6 py-4 text-center">
                  <div class="flex justify-center gap-2">
                    <button @click="openModal(producto)"
                      class="text-xs font-medium text-gray-600 hover:text-blue-600 px-3 py-1.5 rounded-md hover:bg-blue-50 transition-all">
                      Editar
                    </button>
                    <!-- <button @click="confirmDelete(producto)"
                      class="text-xs font-medium text-gray-600 hover:text-red-600 px-3 py-1.5 rounded-md hover:bg-red-50 transition-all">
                      Eliminar
                    </button> -->
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="text-center py-16">
          <p class="text-gray-500">No se encontraron productos</p>
          <p class="text-sm text-gray-400 mt-1">Modifica los filtros para ampliar la búsqueda</p>
        </div>

        <!-- Paginación -->
        <div v-if="pagination && pagination.total > 0"
          class="px-6 py-4 border-t border-gray-200 flex justify-between items-center">
          <div class="text-sm text-gray-500">
            Mostrando {{ pagination.from || 0 }} - {{ pagination.to || 0 }} de {{ pagination.total }} productos
          </div>
          <div class="flex gap-2">
            <button @click="cambiarPagina(pagination.previousPage)" :disabled="!pagination.previousPage"
              class="px-3 py-1 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              Anterior
            </button>
            <span class="px-3 py-1 text-sm bg-gray-100 rounded-lg">
              Página {{ pagination.current_page || 1 }}
            </span>
            <button @click="cambiarPagina(pagination.nextPage)" :disabled="!pagination.nextPage"
              class="px-3 py-1 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              Siguiente
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal para subir Excel -->
    <div v-if="showExcelModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="cerrarModalExcel">
      <div class="bg-white rounded-xl w-full max-w-lg">
        <div class="border-b border-gray-200 px-6 py-5 flex justify-between items-center">
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Subir Productos desde Excel</h2>
            <p class="text-sm text-gray-500">Selecciona un archivo Excel (.xlsx, .xls) con el formato requerido</p>
          </div>
          <button @click="cerrarModalExcel" class="text-gray-400 hover:text-gray-600 text-2xl leading-none">✕</button>
        </div>

        <div class="p-6">
          <!-- Área de drag & drop -->
          <div @dragover.prevent="dragOver = true" @dragleave.prevent="dragOver = false" @drop.prevent="handleDrop"
            :class="dragOver ? 'border-gray-600 bg-gray-100' : 'border-gray-300 bg-gray-50'"
            class="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer hover:bg-gray-100 transition-colors"
            @click="$refs.fileInput.click()">
            <input ref="fileInput" type="file" accept=".xlsx,.xls" @change="handleFileUpload" class="hidden" />
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <p class="mt-2 text-sm text-gray-600">
              Arrastra y suelta tu archivo aquí, o <span class="text-gray-900 font-medium">haz clic para
                seleccionar</span>
            </p>
            <p class="mt-1 text-xs text-gray-500">
              Formatos aceptados: .xlsx, .xls (máx. 10MB)
            </p>
          </div>

          <!-- Mostrar archivo seleccionado -->
          <div v-if="archivoExcel" class="mt-4 p-3 bg-gray-100 rounded-lg">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-sm text-gray-700">{{ archivoExcel.name }}</span>
              </div>
              <button @click="archivoExcel = null; $refs.fileInput.value = ''"
                class="text-red-500 hover:text-red-700">✕</button>
            </div>
          </div>

          <!-- Barra de progreso -->
          <div v-if="subiendoExcel" class="mt-4">
            <div class="flex justify-between text-sm text-gray-600 mb-1">
              <span>Subiendo y procesando...</span>
              <span>{{ progresoCarga }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div class="bg-gray-900 h-2 rounded-full transition-all duration-300"
                :style="{ width: progresoCarga + '%' }"></div>
            </div>
          </div>

          <!-- Mensaje de resultado -->
          <div v-if="resultadoExcel" class="mt-4 p-3 rounded-lg"
            :class="resultadoExcel.tipo === 'exito' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'">
            <div class="flex items-start gap-2">
              <svg v-if="resultadoExcel.tipo === 'exito'" class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none"
                stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <svg v-else class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div class="flex-1">
                <p class="text-sm font-medium">{{ resultadoExcel.mensaje }}</p>
                <div v-if="resultadoExcel.detalles && resultadoExcel.detalles.length" class="mt-2 text-xs">
                  <p class="font-medium">Detalles:</p>
                  <ul class="list-disc list-inside">
                    <li v-for="detalle in resultadoExcel.detalles.slice(0, 5)" :key="detalle">{{ detalle }}</li>
                    <li v-if="resultadoExcel.detalles.length > 5" class="text-gray-500">... y {{
                      resultadoExcel.detalles.length - 5 }} más</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="border-t border-gray-200 px-6 py-4 bg-gray-50 flex justify-end gap-3">
          <button @click="cerrarModalExcel"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            Cancelar
          </button>
          <button @click="subirExcel" :disabled="!archivoExcel || subiendoExcel"
            class="px-4 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed">
            {{ subiendoExcel ? 'Procesando...' : 'Subir Productos' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Product Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="btnCerrarModal">
      <div class="bg-white rounded-xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden">
        <div class="border-b border-gray-200 px-6 py-5 flex justify-between items-center bg-white">
          <div>
            <h2 class="text-lg font-semibold text-gray-900">
              {{ selectedProducto?.id ? "Actualizar Producto" : "Crear Nuevo Producto" }}
            </h2>
            <p class="text-sm text-gray-500">{{ selectedProducto?.id ? "Modifica los datos del producto" : "Ingresa los datos del nuevo producto" }}</p>
          </div>
          <button @click="btnCerrarModal" class="text-gray-400 hover:text-gray-600 text-2xl leading-none">✕</button>
        </div>

        <div class="flex-1 overflow-y-auto p-6">
          <form @submit.prevent="btnConfirmar" class="space-y-6">
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="text-sm font-semibold text-gray-700 mb-4">Información del Producto</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="md:col-span-2">
                  <label class="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Nombre del
                    Producto <span class="text-red-500">*</span></label>
                  <input v-model="selectedProducto.nombre_producto" type="text"
                    class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none" />
                  <p v-if="errors.nombre_producto" class="text-xs text-red-500 mt-1">{{ errors.nombre_producto }}</p>
                </div>

                <div>
                  <label class="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Cantidad <span
                      class="text-red-500">*</span></label>
                  <input v-model.number="selectedProducto.cantidad_producto" type="number" min="0"
                    :disabled="selectedProducto?.id ? true : false"
                    :class="selectedProducto?.id ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'"
                    class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none" />
                  <p v-if="errors.cantidad_producto" class="text-xs text-red-500 mt-1">{{ errors.cantidad_producto }}
                  </p>
                  <p v-if="selectedProducto?.id" class="text-xs text-amber-600 mt-1">La cantidad no se puede modificar
                  </p>
                </div>

                <div>
                  <label class="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Estado</label>
                  <select v-model="selectedProducto.estado"
                    class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none bg-white">
                    <option :value="true">Activo</option>
                    <option :value="false">Inactivo</option>
                  </select>
                </div>
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="text-sm font-semibold text-gray-700 mb-4">Información de Precios</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Precio Compra
                    <span class="text-red-500">*</span></label>
                  <div class="relative">
                    <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 text-sm">S/</span>
                    <input v-model.number="selectedProducto.costo_producto" type="number" step="0.01" min="0"
                      class="w-full pl-7 pr-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none" />
                  </div>
                  <p v-if="errors.costo_producto" class="text-xs text-red-500 mt-1">{{ errors.costo_producto }}</p>
                </div>

                <div>
                  <label class="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Precio Venta <span
                      class="text-red-500">*</span></label>
                  <div class="relative">
                    <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 text-sm">S/</span>
                    <input v-model.number="selectedProducto.precio_unitario" type="number" step="0.01" min="0"
                      class="w-full pl-7 pr-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none" />
                  </div>
                  <p v-if="errors.precio_unitario" class="text-xs text-red-500 mt-1">{{ errors.precio_unitario }}</p>
                </div>
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="text-sm font-semibold text-gray-700 mb-4">Información Adicional</h4>
              <div>
                <label class="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Código de
                  Barra</label>
                <input v-model="selectedProducto.codigo_barra" type="text" :disabled="esCodigoBarraNoEditable"
                  :class="esCodigoBarraNoEditable ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'"
                  class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none font-mono" />
                <p class="text-xs text-gray-400 mt-1">
                  Código único para identificación del producto
                  <span v-if="esCodigoBarraNoEditable" class="text-amber-600"> (No editable porque ya tiene un código
                    asignado)</span>
                  <span v-if="selectedProducto?.id && !selectedProducto?.codigo_barra" class="text-blue-600"> (Puedes
                    asignar un código porque está vacío)</span>
                </p>
              </div>

              <!-- Campo opcional: Código Interno (solo lectura) -->
              <div v-if="selectedProducto?.id" class="mt-4 pt-4 border-t border-gray-200">
                <label class="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">Código Interno del
                  Sistema</label>
                <input :value="selectedProducto.codigo_interno" type="text" disabled
                  class="w-full px-3 py-2 text-sm bg-gray-100 border border-gray-300 rounded-lg font-mono cursor-not-allowed" />
                <p class="text-xs text-gray-400 mt-1">Código generado automáticamente por el sistema</p>
              </div>
            </div>

            <div v-if="selectedProducto.id" class="bg-gray-50 rounded-lg p-4">
              <h4 class="text-sm font-semibold text-gray-700 mb-4">Auditoría</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-500">Fecha de creación:</span>
                  <span class="ml-2 text-gray-700">{{ formatDate(selectedProducto.fecha_creacion) }}</span>
                </div>
                <div>
                  <span class="text-gray-500">Última actualización:</span>
                  <span class="ml-2 text-gray-700">{{ formatDate(selectedProducto.fecha_actualizacion) }}</span>
                </div>
              </div>
            </div>
          </form>
        </div>

        <div class="border-t border-gray-200 px-6 py-4 bg-gray-50 flex justify-end gap-3">
          <button @click="btnCerrarModal"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            Cancelar
          </button>
          <button @click="btnConfirmar" :disabled="guardando"
            class="px-4 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed">
            {{ guardando ? 'Guardando...' : (selectedProducto?.id ? "Actualizar" : "Crear") }}
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showDeleteModal = false">
      <div class="bg-white rounded-xl w-full max-w-md">
        <div class="p-6">
          <div class="flex items-center justify-center mb-4">
            <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
          </div>
          <h3 class="text-lg font-semibold text-center text-gray-800 mb-2">Confirmar eliminación</h3>
          <p class="text-sm text-gray-600 text-center mb-6">
            ¿Estás seguro de que deseas eliminar el producto "{{ productoAEliminar?.nombre_producto }}"?<br>
            Esta acción no se puede deshacer.
          </p>
          <div class="flex gap-3">
            <button @click="showDeleteModal = false"
              class="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
              Cancelar
            </button>
            <button @click="eliminarProducto"
              class="flex-1 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700">
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
  importar_productos_excel  // 👈 Importa la función
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
      filtroBusqueda: "",
      filtroEstado: "todos",
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
  },
  mounted() {
    this.cargarProductos();
  },
  beforeDestroy() {
    if (this.searchTimeout) {
      clearTimeout(this.searchTimeout);
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

        // 👈 Usar la función importada del API
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
          // Recargar la lista de productos
          await this.cargarProductos();
          // Cerrar modal después de 3 segundos
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
        console.error('Error subiendo Excel:', error);
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

    async cargarProductos() {
      this.loading = true;
      this.buscando = false;

      try {
        const params = {};
        if (this.filtroBusqueda) params.search = this.filtroBusqueda;
        if (this.filtroEstado !== "todos") params.estado = this.filtroEstado;

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