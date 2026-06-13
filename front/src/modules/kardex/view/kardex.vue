<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 px-8 py-6">
      <div class="flex justify-between items-start">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center flex-shrink-0">
            <span class="text-white text-xs font-bold">K</span>
          </div>
          <div>
            <h1 class="text-base sm:text-xl font-semibold text-gray-800 tracking-tight">Kardex de Inventario</h1>
            <p class="text-xs text-gray-500 hidden sm:block">Gestión y control de movimientos de stock</p>
          </div>
        </div>
        <!-- <div class="flex gap-3">
          <button class="px-5 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
            </svg>
            Exportar
          </button>
        </div> -->
      </div>
    </header>

    <!-- Main Content -->
    <main class="px-8 py-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
        <span class="ml-3 text-gray-600">Cargando movimientos...</span>
      </div>

      <div v-else>
        <!-- KPI Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div class="bg-white rounded-lg border border-gray-200 p-5">
            <div class="flex justify-between items-start">
              <div>
                <p class="text-xs font-medium text-gray-500  tracking-wide">Total Movimientos</p>
                <p class="text-2xl font-bold text-gray-900 mt-2">{{ totalMovimientos }}</p>
              </div>
              <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg border border-gray-200 p-5">
            <div class="flex justify-between items-start">
              <div>
                <p class="text-xs font-medium text-gray-500  tracking-wide">Ingresos Totales</p>
                <p class="text-2xl font-bold text-emerald-600 mt-2">{{ totalIngresos }}</p>
              </div>
              <div class="w-10 h-10 bg-emerald-50 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                </svg>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg border border-gray-200 p-5">
            <div class="flex justify-between items-start">
              <div>
                <p class="text-xs font-medium text-gray-500  tracking-wide">Salidas Totales</p>
                <p class="text-2xl font-bold text-rose-600 mt-2">{{ totalSalidas }}</p>
              </div>
              <div class="w-10 h-10 bg-rose-50 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-rose-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Filters Panel -->
        <div class="bg-white rounded-lg border border-gray-200 mb-8">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-xs font-semibold text-gray-700 flex items-center gap-2">
              <span class="w-1 h-4 bg-gray-900 rounded-full"></span>
              Filtro de busqueda
            </h2>
          </div>
          
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              <div>
                <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Tipo de Movimiento</label>
                <select v-model="filters.tipoMovimiento" class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none bg-white">
                  <option value="">Todos</option>
                  <option value="1">Ingresos</option>
                  <option value="2">Salidas</option>
                </select>
              </div>
              
              <div>
                <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Origen del Movimiento</label>
                <select v-model="filters.origen" class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none bg-white">
                  <option value="">Todos</option>
                  <option v-for="tipo in tiposMovimiento" :key="tipo.codigo" :value="tipo.codigo">
                    {{ tipo.nombre }}
                  </option>
                </select>
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Producto / Código</label>
                <input 
                  v-model="filters.search"
                  type="text"
                  placeholder="Buscar por nombre o código..."
                  class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none"
                  @keyup.enter="aplicarFiltros"
                >
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Fecha desde</label>
                <input v-model="filters.fechaInicio" type="date" class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none">
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-500  tracking-wide mb-1">Fecha hasta</label>
                <input v-model="filters.fechaFin" type="date" class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-1 focus:ring-gray-400 focus:border-gray-400 outline-none">
              </div>
            </div>
            
            <div class="flex justify-end gap-3 mt-5 pt-2">
              <button @click="resetFilters" class="px-4 py-2 text-xs font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors">
                Limpiar filtros
              </button>
              <button @click="aplicarFiltros" class="px-4 py-2 text-xs font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-800 transition-colors">
                Aplicar filtros
              </button>
            </div>
            
            <div v-if="filtrosActivos" class="mt-4 pt-4 border-t border-gray-100 flex items-center gap-2 flex-wrap">
              <span class="text-xs text-gray-500">Filtros activos:</span>
              <span v-if="filters.tipoMovimiento" class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700">
                {{ filters.tipoMovimiento === '1' ? 'Ingresos' : 'Salidas' }}
              </span>
              <span v-if="filters.origen" class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700">
                {{ getOrigenTexto(filters.origen) }}
              </span>
              <span v-if="filters.search" class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700">
                Búsqueda: {{ filters.search }}
              </span>
              <span v-if="filters.fechaInicio || filters.fechaFin" class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700">
                {{ filters.fechaInicio || 'Inicio' }} - {{ filters.fechaFin || 'Fin' }}
              </span>
              <button @click="resetFilters" class="text-xs text-red-400 hover:text-red-600 ml-2">
                Limpiar todo
              </button>
            </div>
          </div>
        </div>

        <!-- Transactions Table -->
        <div class="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
            <h2 class="text-xs font-semibold text-gray-700 flex items-center gap-2">
              <span class="w-1 h-4 bg-gray-900 rounded-full"></span>
              Historial de movimientos
            </h2>
            <span class="text-xs text-gray-500">{{ pagination.total || 0 }} resultados</span>
          </div>
          
          <div class="overflow-x-auto" v-if="kardexData.length > 0">
            <table class="w-full">
              <thead class="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Fecha</th>
                  <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Tipo</th>
                  <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Origen</th>
                  <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Producto</th>
                  <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Código Barra</th>
                  <th class="text-right px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Cantidad</th>
                  <th class="text-right px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Stock Ant.</th>
                  <th class="text-right px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Stock Act.</th>
                  <th class="text-right px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Precio Compra</th>
                  <th class="text-right px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Precio Venta</th>
                  <th class="text-right px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Subtotal</th>
                  <th class="text-center px-6 py-3 text-xs font-semibold text-gray-500  tracking-wider">Referencia</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="item in kardexData" :key="item.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-6 py-4 whitespace-nowrap text-xs text-gray-600">{{ formatDate(item.fecha_movimiento) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="item.origen_movimiento.tipo === 1 ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'" class="px-2 py-1 text-xs rounded-full">
                      {{ item.origen_movimiento.tipo === 1 ? 'Ingreso' : 'Salida' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-xs text-gray-700 font-medium">
                    {{ item.origen_movimiento.nombre }}
                  </td>
                  <td class="px-6 py-4 text-xs text-gray-700 max-w-[200px] truncate" :title="item.nombre_producto">{{ item.nombre_producto }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-xs text-gray-500">{{ item.codigo_barra || "Sin código" }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-xs font-semibold" :class="item.origen_movimiento.tipo === 1 ? 'text-emerald-600' : 'text-rose-600'">
                    {{ item.origen_movimiento.tipo === 1 ? '+' : '-' }} {{ item.cantidad }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-xs text-gray-600">{{ item.stock_anterior }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-xs font-medium text-gray-800">{{ item.stock_nuevo }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-xs text-gray-600">S/ {{ formatPrice(item.precio_compra) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-xs text-gray-600">S/ {{ formatPrice(item.precio_venta) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-xs font-medium text-gray-700">S/ {{ formatPrice(item.subtotal) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-center text-xs">
                    <span class="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">{{ item.correlativo_referencia || '-' }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div v-else class="text-center py-16">
            <p class="text-gray-500">No se encontraron movimientos</p>
            <p class="text-xs text-gray-400 mt-1">Modifica los filtros para ampliar la búsqueda</p>
          </div>

          <!-- Paginación -->
          <div v-if="pagination.total > 0" class="px-6 py-4 border-t border-gray-200 flex justify-between items-center">
            <div class="text-xs text-gray-500">
              Mostrando {{ pagination.from || 0 }} - {{ pagination.to || 0 }} de {{ pagination.total || 0 }} resultados
            </div>
            <div class="flex gap-2">
              <button 
                @click="cambiarPagina(pagination.previous)" 
                :disabled="!pagination.previous"
                class="px-3 py-1 text-xs border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                Anterior
              </button>
              <span class="px-3 py-1 text-xs bg-gray-100 rounded-lg">
                Página {{ pagination.current_page || 1 }} de {{ pagination.total_pages || 1 }}
              </span>
              <button 
                @click="cambiarPagina(pagination.next)" 
                :disabled="!pagination.next"
                class="px-3 py-1 text-xs border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                Siguiente
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { list_kardex, list_tipo_movimientos } from '../api/kardex'

export default {
  name: 'KardexModule',
  data() {
    return {
      loading: false,
      kardexData: [],
      tiposMovimiento: [],
      filters: {
        tipoMovimiento: '',
        origen: '',
        search: '',
        fechaInicio: '',
        fechaFin: ''
      },
      pagination: {
        current_page: 1,
        total_pages: 1,
        total: 0,
        from: 0,
        to: 0,
        previous: null,
        next: null
      }
    }
  },
  computed: {
    totalMovimientos() {
      return this.pagination.total || 0
    },
    totalIngresos() {
      return this.kardexData.filter(item => item.origen_movimiento?.tipo === 1).length
    },
    totalSalidas() {
      return this.kardexData.filter(item => item.origen_movimiento?.tipo === 2).length
    },
    filtrosActivos() {
      return this.filters.tipoMovimiento || 
             this.filters.origen || 
             this.filters.search || 
             this.filters.fechaInicio || 
             this.filters.fechaFin
    }
  },
  mounted() {
    this.cargarTiposMovimiento()
    this.cargarKardex()
  },
  methods: {
    async cargarTiposMovimiento() {
      try {
        const response = await list_tipo_movimientos()
        this.tiposMovimiento = response.data
      } catch (error) {
        console.error('Error al cargar tipos de movimiento:', error)
      }
    },
    async cargarKardex(url = null) {
      this.loading = true
      
      try {
        const params = {}
        
        if (this.filters.tipoMovimiento) {
          params.tipo_movimiento = this.filters.tipoMovimiento
        }
        if (this.filters.origen) {
          params.origen = this.filters.origen
        }
        if (this.filters.search) {
          params.search = this.filters.search
        }
        if (this.filters.fechaInicio) {
          params.fecha_desde = this.filters.fechaInicio
        }
        if (this.filters.fechaFin) {
          params.fecha_hasta = this.filters.fechaFin
        }
        
        let response
        if (url) {
          const urlObj = new URL(url, window.location.origin)
          const searchParams = new URLSearchParams(urlObj.search)
          const pageParams = {}
          for (let [key, value] of searchParams) {
            pageParams[key] = value
          }
          response = await list_kardex({ ...params, ...pageParams })
        } else {
          response = await list_kardex(params)
        }
        
        this.kardexData = response.data.results || []
        this.pagination = {
          current_page: this.getPageNumberFromUrl(response.data.previous, response.data.next),
          total_pages: Math.ceil((response.data.count || 0) / 10),
          total: response.data.count || 0,
          from: response.data.results?.length > 0 ? (this.getPageNumberFromUrl(response.data.previous, response.data.next) - 1) * 10 + 1 : 0,
          to: Math.min(this.getPageNumberFromUrl(response.data.previous, response.data.next) * 10, response.data.count || 0),
          previous: response.data.previous,
          next: response.data.next
        }
      } catch (error) {
        console.error('Error al cargar kardex:', error)
        this.kardexData = []
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
    cambiarPagina(url) {
      if (url) {
        this.cargarKardex(url)
      }
    },
    formatDate(dateString) {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return date.toLocaleDateString('es-ES', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    formatPrice(price) {
      if (!price && price !== 0) return '0.00'
      return Number(price).toFixed(2)
    },
    getOrigenTexto(codigo) {
      const tipo = this.tiposMovimiento.find(t => t.codigo === codigo)
      return tipo ? tipo.nombre : codigo
    },
    resetFilters() {
      this.filters = {
        tipoMovimiento: '',
        origen: '',
        search: '',
        fechaInicio: '',
        fechaFin: ''
      }
      this.cargarKardex()
    },
    aplicarFiltros() {
      this.cargarKardex()
    }
  }
}
</script>