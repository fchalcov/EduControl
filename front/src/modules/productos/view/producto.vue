<template>
    <div class="h-screen bg-gray-50 flex flex-col">
        <!-- Header -->
        <div class="bg-white border-b border-gray-200 px-4 md:px-6 py-4 sticky top-0 z-10 shadow-sm">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                <div>
                    <h1 class="text-lg md:text-xl font-semibold text-gray-800">
                        Gestión de Productos
                    </h1>
                    <p class="text-xs md:text-sm text-gray-500 mt-0.5">
                        Administración del inventario de productos
                    </p>
                </div>

                <button @click="openModal(null)"
                    class="w-full md:w-auto inline-flex justify-center items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg shadow-sm transition-all duration-200">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    Nuevo Producto
                </button>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex-1 flex items-center justify-center">
            <div class="text-center">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <p class="mt-2 text-gray-500">Cargando productos...</p>
            </div>
        </div>

        <!-- Tabla -->
        <div v-else class="flex-1 px-4 md:px-6 py-4 md:py-6">
            <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                <!-- Filtros y búsqueda -->
                <div class="p-4 border-b border-gray-200 bg-gray-50">
                    <div class="flex flex-col sm:flex-row gap-3">
                        <div class="flex-1">
                            <div class="relative">
                                <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                </svg>
                                <input 
                                    v-model="filtroBusqueda" 
                                    @input="onSearchInput"
                                    @keyup.esc="limpiarBusqueda"
                                    type="text" 
                                    placeholder="Buscar por nombre o código de barras..."
                                    class="w-full pl-9 pr-10 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
                                />
                                <!-- Indicador de búsqueda en tiempo real -->
                                <div v-if="buscando" 
                                     class="absolute right-3 top-1/2 transform -translate-y-1/2">
                                    <svg class="animate-spin h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                </div>
                            </div>
                        </div>
                        <select v-model="filtroEstado" @change="onFilterChange" class="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                            <option value="todos">Todos los estados</option>
                            <option value="true">Activos</option>
                            <option value="false">Inactivos</option>
                        </select>
                        <button 
                            v-if="filtroBusqueda"
                            @click="limpiarBusqueda"
                            class="px-3 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                            Limpiar
                        </button>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="min-w-[900px] w-full">
                        <thead class="bg-gray-50 border-b border-gray-200">
                            <tr>
                                <th class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Producto
                                </th>
                                <th class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Cantidad
                                </th>
                                <th class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    P.Compra
                                </th>
                                <th class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    P.Venta
                                </th>
                                <th class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Código de Barra
                                </th>
                                <th class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Estado
                                </th>
                                <th class="px-4 md:px-6 py-4 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Acciones
                                </th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            <tr v-for="producto in productos" :key="producto.id" class="hover:bg-gray-50 transition-colors">
                                <td class="px-4 md:px-6 py-4">
                                    <div class="flex flex-col">
                                        <span class="text-sm font-medium text-gray-900">
                                            {{ producto.nombre_producto }}
                                        </span>
                                    </div>
                                </td>
                                <td class="px-4 md:px-6 py-4 whitespace-nowrap">
                                    <span class="text-sm text-gray-900 font-medium">
                                        {{ producto.cantidad_producto }}
                                    </span>
                                </td>
                                <td class="px-4 md:px-6 py-4 whitespace-nowrap">
                                    <span class="text-sm text-gray-900">
                                        S/{{ formatNumber(producto.costo_producto) }}
                                    </span>
                                </td>
                                <td class="px-4 md:px-6 py-4 whitespace-nowrap">
                                    <span class="text-sm font-semibold text-green-600">
                                        S/{{ formatNumber(producto.precio_unitario) }}
                                    </span>
                                </td>
                                <td class="px-4 md:px-6 py-4">
                                    <code class="text-xs bg-gray-100 px-2 py-1 rounded">
                                        {{ producto.codigo_barra || "Sin código" }}
                                    </code>
                                </td>
                                <td class="px-4 md:px-6 py-4 whitespace-nowrap">
                                    <span :class="producto.estado
                                            ? 'bg-green-100 text-green-800'
                                            : 'bg-gray-100 text-gray-600'
                                        " class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium">
                                        <span :class="producto.estado ? 'bg-green-500' : 'bg-gray-400'"
                                            class="w-1.5 h-1.5 rounded-full"></span>
                                        {{ producto.estado ? "Activo" : "Inactivo" }}
                                    </span>
                                </td>
                                <td class="px-4 md:px-6 py-4 text-center">
                                    <div class="flex justify-center gap-2">
                                        <button @click="openModal(producto)"
                                            class="text-xs font-medium text-gray-600 hover:text-blue-600 px-3 py-1.5 rounded-md hover:bg-blue-50 transition-all">
                                            Editar
                                        </button>
                                        <button @click="confirmDelete(producto)"
                                            class="text-xs font-medium text-gray-600 hover:text-red-600 px-3 py-1.5 rounded-md hover:bg-red-50 transition-all">
                                            Eliminar
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            <tr v-if="productos && productos.length === 0">
                                <td colspan="7" class="px-6 py-12 text-center text-gray-500">
                                    No se encontraron productos
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Paginación -->
                <div v-if="pagination && pagination.total > 0" class="px-6 py-4 border-t border-gray-200 bg-gray-50">
                    <div class="flex items-center justify-between flex-wrap gap-2">
                        <div class="text-sm text-gray-600">
                            Mostrando {{ pagination.from || 0 }} - {{ pagination.to || 0 }} de {{ pagination.total || 0 }} productos
                        </div>
                        <div class="flex gap-2">
                            <button 
                                @click="cambiarPagina(pagination.previousPage)"
                                :disabled="!pagination.previousPage"
                                class="px-3 py-1 text-sm border rounded-lg hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed">
                                Anterior
                            </button>
                            <button 
                                @click="cambiarPagina(pagination.nextPage)"
                                :disabled="!pagination.nextPage"
                                class="px-3 py-1 text-sm border rounded-lg hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed">
                                Siguiente
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal de Producto -->
        <div v-if="showModal" class="fixed inset-0 z-50 overflow-y-auto">
            <div class="fixed inset-0 bg-black/50 backdrop-blur-sm" @click="btnCerrarModal"></div>

            <div class="flex min-h-full items-center justify-center p-4">
                <div class="relative bg-white w-full max-w-4xl rounded-xl shadow-2xl flex flex-col max-h-[90vh]">
                    <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-white rounded-t-xl">
                        <div>
                            <h3 class="text-lg font-semibold text-gray-800">
                                {{ selectedProducto?.id ? "Actualizar Producto" : "Crear Nuevo Producto" }}
                            </h3>
                            <p class="text-sm text-gray-500">
                                {{ selectedProducto?.id ? "Modifica los datos del producto" : "Ingresa los datos del nuevo producto" }}
                            </p>
                        </div>
                        <button @click="btnCerrarModal"
                            class="text-gray-400 hover:text-gray-600 transition-colors p-1 rounded-lg hover:bg-gray-100 text-2xl">
                            ×
                        </button>
                    </div>

                    <div class="flex-1 overflow-y-auto p-6">
                        <form @submit.prevent="btnConfirmar" class="space-y-6">
                            <div class="bg-gray-50 rounded-lg p-4">
                                <h4 class="text-sm font-semibold text-gray-700 mb-4 flex items-center gap-2">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    Información del Producto
                                </h4>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div class="md:col-span-2">
                                        <label class="block text-sm font-medium text-gray-700 mb-1">
                                            Nombre del Producto <span class="text-red-500">*</span>
                                        </label>
                                        <input v-model="selectedProducto.nombre_producto" type="text"
                                            class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                                            placeholder="Ej: Laptop HP Pavilion" />
                                        <p v-if="errors.nombre_producto" class="text-xs text-red-500 mt-1">{{ errors.nombre_producto }}</p>
                                    </div>

                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">
                                            Cantidad <span class="text-red-500">*</span>
                                        </label>
                                        <input v-model.number="selectedProducto.cantidad_producto" type="number" min="0"
                                            class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
                                        <p v-if="errors.cantidad_producto" class="text-xs text-red-500 mt-1">{{ errors.cantidad_producto }}</p>
                                    </div>

                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">
                                            Estado
                                        </label>
                                        <select v-model="selectedProducto.estado"
                                            class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white">
                                            <option :value="true">Activo</option>
                                            <option :value="false">Inactivo</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <div class="bg-gray-50 rounded-lg p-4">
                                <h4 class="text-sm font-semibold text-gray-700 mb-4 flex items-center gap-2">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    Información de Precios
                                </h4>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">
                                            Precio Compra <span class="text-red-500">*</span>
                                        </label>
                                        <div class="relative">
                                            <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">S/</span>
                                            <input v-model.number="selectedProducto.costo_producto" type="number" step="0.01" min="0"
                                                class="w-full pl-7 pr-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
                                        </div>
                                        <p v-if="errors.costo_producto" class="text-xs text-red-500 mt-1">{{ errors.costo_producto }}</p>
                                    </div>

                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">
                                            Precio Venta <span class="text-red-500">*</span>
                                        </label>
                                        <div class="relative">
                                            <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">S/</span>
                                            <input v-model.number="selectedProducto.precio_unitario" type="number" step="0.01" min="0"
                                                class="w-full pl-7 pr-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
                                        </div>
                                        <p v-if="errors.precio_unitario" class="text-xs text-red-500 mt-1">{{ errors.precio_unitario }}</p>
                                    </div>
                                </div>
                            </div>

                            <div class="bg-gray-50 rounded-lg p-4">
                                <h4 class="text-sm font-semibold text-gray-700 mb-4 flex items-center gap-2">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                                    </svg>
                                    Información Adicional
                                </h4>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">
                                        Código de Barra
                                    </label>
                                    <input v-model="selectedProducto.codigo_barra" type="text"
                                        class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono"
                                        placeholder="Ej: 7891234567890" />
                                    <p class="text-xs text-gray-500 mt-1">Código único para identificación del producto</p>
                                </div>
                            </div>

                            <div v-if="selectedProducto.id" class="bg-gray-50 rounded-lg p-4">
                                <h4 class="text-sm font-semibold text-gray-700 mb-4 flex items-center gap-2">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    Auditoría
                                </h4>
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

                    <div class="flex flex-col sm:flex-row justify-end gap-3 px-6 py-4 border-t border-gray-200 bg-gray-50 rounded-b-xl">
                        <button @click="btnCerrarModal"
                            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                            Cancelar
                        </button>
                        <button @click="btnConfirmar"
                            :disabled="guardando"
                            class="px-6 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed">
                            {{ guardando ? 'Guardando...' : (selectedProducto?.id ? "Actualizar" : "Crear") }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal de confirmación de eliminación -->
        <div v-if="showDeleteModal" class="fixed inset-0 z-50 overflow-y-auto">
            <div class="fixed inset-0 bg-black/50 backdrop-blur-sm" @click="showDeleteModal = false"></div>
            <div class="flex min-h-full items-center justify-center p-4">
                <div class="relative bg-white w-full max-w-md rounded-xl shadow-2xl">
                    <div class="p-6">
                        <div class="flex items-center justify-center mb-4">
                            <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                                <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                            </div>
                        </div>
                        <h3 class="text-lg font-semibold text-center text-gray-800 mb-2">
                            Confirmar eliminación
                        </h3>
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
    </div>
</template>

<script>
import { 
    list_producto, 
    create_producto, 
    update_producto, 
    delete_producto,
    get_producto 
} from '../api/producto.ts';

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
            // Variables para debounce
            searchTimeout: null,
            buscando: false,
        };
    },
    mounted() {
        this.cargarProductos();
    },
    beforeDestroy() {
        // Limpiar timeout al destruir el componente
        if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
        }
    },
    methods: {
        // Método para manejar la búsqueda con debounce
        onSearchInput() {
            // Limpiar timeout anterior
            if (this.searchTimeout) {
                clearTimeout(this.searchTimeout);
            }
            
            // Si el campo está vacío, buscar inmediatamente
            if (!this.filtroBusqueda.trim()) {
                this.cargarProductos();
                return;
            }
            
            // Mostrar indicador de búsqueda
            this.buscando = true;
            
            // Esperar a que el usuario termine de escribir (500ms)
            this.searchTimeout = setTimeout(() => {
                this.cargarProductos();
            }, 500);
        },
        
        // Método para manejar cambios en el filtro de estado
        onFilterChange() {
            this.cargarProductos();
        },
        
        // Método para limpiar la búsqueda
        limpiarBusqueda() {
            this.filtroBusqueda = "";
            this.cargarProductos();
        },
        
        async cargarProductos() {
            this.loading = true;
            this.buscando = false; // Ocultar indicador de búsqueda
            
            try {
                const params = {};
                if (this.filtroBusqueda) params.search = this.filtroBusqueda;
                if (this.filtroEstado !== "todos") params.estado = this.filtroEstado;
                
                const response = await list_producto(params);
            
                if (response.data && response.data.results) {
                    this.productos = response.data.results || [];
                    this.pagination = {
                        count: response.data.count || 0,
                        next: response.data.next,
                        previous: response.data.previous,
                        nextPage: response.data.next,
                        previousPage: response.data.previous,
                        from: 1,
                        to: response.data.results.length,
                        total: response.data.count || 0
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
                
                const response = await list_producto(params);
                
                if (response.data && response.data.results) {
                    this.productos = response.data.results || [];
                    this.pagination = {
                        count: response.data.count || 0,
                        next: response.data.next,
                        previous: response.data.previous,
                        nextPage: response.data.next,
                        previousPage: response.data.previous,
                        from: this.pagination?.from || 1,
                        to: response.data.results.length || 0,
                        total: response.data.count || 0
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

            if (this.selectedProducto.cantidad_producto < 0) {
                this.errors.cantidad_producto = "La cantidad no puede ser negativa";
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
                    await update_producto(this.selectedProducto.id, this.selectedProducto);
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
            if (!value && value !== 0) return "0.00";
            return new Intl.NumberFormat('es-MX', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
            }).format(parseFloat(value));
        },

        formatDate(dateString) {
            if (!dateString) return "N/A";
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
            }).format(date);
        },
    },
};
</script>
