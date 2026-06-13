<template>
    <div class="bg-gray-50 flex flex-col">
        <!-- Header -->
        <div class="bg-white border-b border-gray-200 px-4 md:px-6 py-4 sticky top-0 z-10 flex-shrink-0">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                <div>
                    <h1 class="text-lg md:text-xl font-semibold text-gray-800">
                        Gestión de Módulos
                    </h1>
                    <p class="text-xs md:text-xs text-gray-500 mt-0.5">
                        Administra la estructura de menús y navegación del sistema
                    </p>
                </div>

                <button @click="openModal(null)"
                    class="w-full md:w-auto inline-flex justify-center items-center gap-2 px-4 py-2 bg-gray-900 hover:bg-gray-900 text-white text-xs font-medium rounded-lg shadow-xs transition-all duration-200">
                    Nuevo Módulo
                </button>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex-1 flex items-center justify-center py-12">
            <div class="text-center">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <p class="mt-2 text-gray-500">Cargando módulos...</p>
            </div>
        </div>

        <!-- Tabla de Módulos -->
        <div v-else class="flex-1 px-4 md:px-6 py-4 md:py-6 overflow-hidden">
            <div class="bg-white rounded-xl border border-gray-200 shadow-xs overflow-hidden h-full flex flex-col">
                <!-- Barra de búsqueda y filtros -->
                <div class="p-4 border-b border-gray-200 bg-gray-50 flex-shrink-0">
                    <div class="flex flex-col sm:flex-row gap-3">
                        <div class="flex-1 relative">
                            <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                            <input type="text" v-model="searchTerm" placeholder="Buscar módulo por nombre..."
                                class="w-full pl-9 pr-4 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
                        </div>
                        <div class="flex gap-2">
                            <button @click="expandAll"
                                class="inline-flex items-center gap-1 px-3 py-2 text-xs text-gray-600 hover:text-blue-600 border border-gray-300 rounded-lg hover:bg-white transition-colors">
                                ▼ Expandir todo
                            </button>
                            <button @click="collapseAll"
                                class="inline-flex items-center gap-1 px-3 py-2 text-xs text-gray-600 hover:text-blue-600 border border-gray-300 rounded-lg hover:bg-white transition-colors">
                                ▲ Colapsar todo
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Tabla principal -->
                <div class="overflow-x-auto flex-1">
                    <table class="min-w-[800px] w-full">
                        <thead class="bg-gray-50 border-b border-gray-200 sticky top-0">
                            <tr>
                                <th
                                    class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600  tracking-wider w-10">
                                </th>
                                <th
                                    class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600  tracking-wider">
                                    Módulo
                                </th>
                                <th
                                    class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600  tracking-wider">
                                    Ruta
                                </th>
                                <th
                                    class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600  tracking-wider">
                                    Estado
                                </th>
                                <th
                                    class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600  tracking-wider">
                                    Orden
                                </th>
                                <th
                                    class="px-4 md:px-6 py-4 text-center text-xs font-semibold text-gray-600  tracking-wider">
                                    Acciones
                                </th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            <template v-for="module in filteredModules" :key="module.id">
                                <!-- Módulo padre -->
                                <tr class="hover:bg-gray-50 transition-colors">
                                    <td class="px-4 md:px-6 py-4 whitespace-nowrap">
                                        <button v-if="module.children?.length" @click="toggleExpand(module.id)"
                                            class="text-gray-400 hover:text-gray-600 transition-transform"
                                            :class="{ 'rotate-90': expandedState[module.id] }">
                                            <component :is="Icons.ChevronRightIcon" class="w-4 h-4" />
                                        </button>
                                        <div v-else class="w-4"></div>
                                    </td>
                                    <td class="px-4 md:px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center gap-2 md:gap-3">
                                            <component :is="getIconComponent(module.icono)"
                                                class="w-5 h-5 text-gray-400" />
                                            <span class="text-xs font-medium text-gray-900">
                                                {{ module.titulo }}
                                            </span>
                                        </div>
                                    </td>
                                    <td class="px-4 md:px-6 py-4">
                                        <code class="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded">
                                            {{ module.ruta || "—" }}
                                        </code>
                                    </td>
                                    <td class="px-4 md:px-6 py-4 whitespace-nowrap">
                                        <span :class="module.activo
                                            ? 'bg-green-100 text-green-800'
                                            : 'bg-gray-100 text-gray-600'
                                            "
                                            class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium">
                                            <span :class="module.activo ? 'bg-green-500' : 'bg-gray-400'"
                                                class="w-1.5 h-1.5 rounded-full"></span>
                                            {{ module.activo ? "Activo" : "Inactivo" }}
                                        </span>
                                    </td>
                                    <td class="px-4 md:px-6 py-4 whitespace-nowrap text-left">
                                        <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                                            {{ module.orden }}
                                        </span>
                                    </td>
                                    <td class="px-4 md:px-6 py-4 text-center">
                                        <div class="flex justify-center gap-2">
                                            <button @click="openModal(module)"
                                                class="text-xs font-medium text-gray-600 hover:text-blue-600 px-3 py-1.5 rounded-md hover:bg-blue-50 transition-all">
                                                Editar
                                            </button>
                                            <button @click="confirmDelete(module)"
                                                class="text-xs font-medium text-gray-600 hover:text-red-600 px-3 py-1.5 rounded-md hover:bg-red-50 transition-all">
                                                Eliminar
                                            </button>
                                        </div>
                                    </td>
                                </tr>

                                <!-- Submódulos -->
                                <tr v-for="child in (expandedState[module.id] ? module.children : [])" :key="child.id"
                                    class="hover:bg-gray-50 transition-colors bg-gray-50/30">
                                    <td class="px-4 md:px-6 py-4 whitespace-nowrap">
                                        <div class="w-4"></div>
                                    </td>
                                    <td class="px-4 md:px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center gap-2 md:gap-3 pl-6 relative">
                                            <div class="flex items-center gap-2 md:gap-3">
                                                <component :is="getIconComponent(child.icono)"
                                                    class="w-5 h-5 text-gray-400" />
                                                <span class="text-xs font-medium text-gray-900">
                                                    {{ child.titulo }}
                                                </span>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-4 md:px-6 py-4">
                                        <code class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                                            {{ child.ruta || "—" }}
                                        </code>
                                    </td>
                                    <td class="px-4 md:px-6 py-4 whitespace-nowrap">
                                        <span :class="child.activo
                                            ? 'bg-green-100 text-green-800'
                                            : 'bg-gray-100 text-gray-600'
                                            "
                                            class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium">
                                            <span :class="child.activo ? 'bg-green-500' : 'bg-gray-400'"
                                                class="w-1.5 h-1.5 rounded-full"></span>
                                            {{ child.activo ? "Activo" : "Inactivo" }}
                                        </span>
                                    </td>
                                    <td class="px-4 md:px-6 py-4 whitespace-nowrap text-left">
                                        <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                                            {{ child.orden }}
                                        </span>
                                    </td>
                                    <td class="px-4 md:px-6 py-4 text-center">
                                        <div class="flex justify-center gap-2">
                                            <button @click="openModal(child)"
                                                class="text-xs font-medium text-gray-600 hover:text-blue-600 px-3 py-1.5 rounded-md hover:bg-blue-50 transition-all">
                                                Editar
                                            </button>
                                            <button @click="confirmDelete(child)"
                                                class="text-xs font-medium text-gray-600 hover:text-red-600 px-3 py-1.5 rounded-md hover:bg-red-50 transition-all">
                                                Eliminar
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            </template>

                            <!-- Mensaje sin resultados -->
                            <tr v-if="filteredModules.length === 0">
                                <td colspan="6" class="px-4 md:px-6 py-12 text-center">
                                    <svg class="w-12 h-12 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                                    </svg>
                                    <p class="text-gray-500">No se encontraron módulos</p>
                                    <p class="text-xs text-gray-400 mt-1">Prueba con otros términos de búsqueda</p>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div v-if="showModal" class="fixed inset-0 z-50 overflow-y-auto">
            <div class="fixed inset-0 bg-black/50 backdrop-blur-xs" @click="btnCerrarModal"></div>

            <div class="flex min-h-full items-center justify-center p-4">
                <div class="relative bg-white w-full max-w-2xl rounded-xl shadow-2xl flex flex-col max-h-[90vh]">
                    <!-- Header -->
                    <div
                        class="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-white rounded-t-xl">
                        <div>
                            <h3 class="text-lg font-semibold text-gray-800">
                                {{ selectedModule?.id ? "Actualizar Módulo" : "Crear Nuevo Módulo" }}
                            </h3>
                            <p class="text-xs text-gray-500">
                                {{
                                    selectedModule?.id
                                        ? "Modifica la configuración del módulo"
                                        : "Ingresa los datos del nuevo módulo"
                                }}
                            </p>
                        </div>
                        <button @click="btnCerrarModal"
                            class="text-gray-400 hover:text-gray-600 transition-colors p-1 rounded-lg hover:bg-gray-100 text-2xl">
                            ×
                        </button>
                    </div>

                    <!-- Body con tabs -->
                    <div class="flex-1 overflow-hidden flex flex-col">
                        <!-- Tabs de navegación -->
                        <div class="border-b border-gray-200 px-6">
                            <div class="flex gap-6 overflow-x-auto">
                                <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key" :class="[
                                    'py-3 text-xs font-medium transition-colors relative whitespace-nowrap',
                                    activeTab === tab.key
                                        ? 'text-blue-600'
                                        : 'text-gray-500 hover:text-gray-700',
                                ]">
                                    {{ tab.label }}
                                    <div v-if="activeTab === tab.key"
                                        class="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600 rounded-full"></div>
                                </button>
                            </div>
                        </div>

                        <div class="flex-1 overflow-y-auto p-6">
                            <!-- Tab: Datos básicos -->
                            <div v-show="activeTab === 'basic'" class="space-y-5 max-w-2xl">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label class="block text-xs font-medium text-gray-700 mb-1">
                                            Título del módulo <span class="text-red-500">*</span>
                                        </label>
                                        <input v-model="selectedModule.titulo" type="text"
                                            class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                                            placeholder="Ej: Usuarios, Cursos, Configuración" />
                                        <p v-if="errors.titulo" class="text-xs text-red-500 mt-1">{{ errors.titulo }}</p>
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-gray-700 mb-1">
                                            Orden <span class="text-red-500">*</span>
                                        </label>
                                        <input v-model.number="selectedModule.orden" type="number"
                                            class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                            placeholder="0" min="0"/>
                                        <p v-if="errors.orden" class="text-xs text-red-500 mt-1">{{ errors.orden }}</p>
                                    </div>
                                </div>

                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label class="block text-xs font-medium text-gray-700 mb-1">
                                            Ruta del módulo
                                        </label>
                                        <input v-model="selectedModule.ruta" type="text"
                                            class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 "
                                            placeholder="Ej: /usuarios/list" />
                                        <p class="text-xs text-gray-400 mt-1">Ruta de navegación</p>
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-gray-700 mb-1">
                                            Estado
                                        </label>
                                        <select v-model="selectedModule.activo"
                                            class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white">
                                            <option :value="true">Activo</option>
                                            <option :value="false">Inactivo</option>
                                        </select>
                                    </div>
                                </div>

                                <div>
                                    <label class="block text-xs font-medium text-gray-700 mb-1">
                                        Módulo padre
                                    </label>
                                    <select v-model="selectedModule.padre_id"
                                        class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white">
                                        <option :value="null">(Ninguno - Módulo principal)</option>
                                        <option v-for="mod in parentModules" :key="mod.id" :value="mod.id"
                                            :disabled="mod.id === selectedModule?.id">
                                            {{ mod.titulo }} (ID: {{ mod.id }})
                                        </option>
                                    </select>
                                    <p class="text-xs text-gray-400 mt-1">Dejar vacío para módulo principal</p>
                                </div>

                                <!-- Vista previa -->
                                <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
                                    <p class="text-xs font-medium text-gray-500  tracking-wider mb-2">Vista previa</p>
                                    <div class="flex items-center gap-3">
                                        <div
                                            class="w-10 h-10 rounded-lg bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center text-white shadow-xs">
                                            <component :is="getIconComponent(selectedModule?.icono)" class="w-5 h-5" />
                                        </div>
                                        <div>
                                            <p class="text-xs font-medium text-gray-900">{{ selectedModule?.titulo }}</p>
                                            <p class="text-xs text-gray-500 ">{{ selectedModule?.ruta || 'Sin ruta' }}</p>
                                        </div>
                                        <span class="ml-auto text-xs text-gray-400">Orden: {{ selectedModule?.orden || 0 }}</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Tab: Icono -->
                            <div v-show="activeTab === 'icon'" class="space-y-5 max-w-2xl">
                                <div>
                                    <label class="block text-xs font-medium text-gray-700 mb-2">Seleccionar Icono</label>
                                    <input v-model="iconSearch" placeholder="Buscar icono..."
                                        class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
                                </div>
                                <div
                                    class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3 max-h-64 overflow-y-auto pr-2">
                                    <div v-for="iconOption in filteredIcons" :key="iconOption.name"
                                        @click="selectedModule.icono = iconOption.name" :class="['flex flex-col items-center gap-2 p-3 rounded-lg border cursor-pointer transition-all',
                                            selectedModule.icono === iconOption.name
                                                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                                                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50']">
                                        <component :is="iconOption.component" class="w-6 h-6 text-gray-600" />
                                        <span class="text-[10px] text-gray-500 text-center break-all">
                                            {{ iconOption.label }}
                                        </span>
                                    </div>
                                </div>
                                <div v-if="selectedModule.icono"
                                    class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg border">
                                    <component :is="getIconComponent(selectedModule.icono)" class="w-6 h-6 text-blue-600" />
                                    <span class="text-xs text-gray-700">
                                        {{ selectedModule.icono }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Footer mejorado -->
                    <div
                        class="flex flex-col sm:flex-row justify-end gap-3 px-6 py-4 border-t border-gray-200 bg-gray-50 rounded-b-xl">
                        <button @click="btnCerrarModal"
                            class="px-4 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                            Cancelar
                        </button>
                        <button @click="btnConfirmar"
                            :disabled="guardando"
                            class="px-6 py-2 text-xs font-medium text-white bg-gray-900 rounded-lg hover:bg-gray-900 transition-colors shadow-xs disabled:opacity-50 disabled:cursor-not-allowed">
                            {{ guardando ? 'Guardando...' : (selectedModule?.id ? "Actualizar" : "Crear") }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal de confirmación de eliminación -->
        <div v-if="showDeleteModal" class="fixed inset-0 z-50 overflow-y-auto">
            <div class="fixed inset-0 bg-black/50 backdrop-blur-xs" @click="showDeleteModal = false"></div>
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
                        <p class="text-xs text-gray-600 text-center mb-6">
                            ¿Estás seguro de que deseas eliminar el módulo "{{ moduleAEliminar?.titulo }}"?<br>
                            Esta acción no se puede deshacer.
                        </p>
                        <div class="flex gap-3">
                            <button @click="showDeleteModal = false"
                                class="flex-1 px-4 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
                                Cancelar
                            </button>
                            <button @click="eliminarModulo"
                                class="flex-1 px-4 py-2 text-xs font-medium text-white bg-red-600 rounded-lg hover:bg-red-700">
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
import { list_menu, save_menu } from "../api/modulo";
import sweetalert2 from "sweetalert2";
import * as Icons from "@heroicons/vue/24/outline";

export default {
    name: "GestionModulos",
    data() {
        return {
            Icons,
            modulesData: [],
            showModal: false,
            showDeleteModal: false,
            selectedModule: {
                titulo: "",
                ruta: null,
                icono: "ListBulletIcon",
                orden: 0,
                activo: true,
                padre_id: null,
            },
            moduleAEliminar: null,
            searchTerm: "",
            expandedState: {},
            activeTab: "basic",
            iconSearch: "",
            errors: {},
            loading: false,
            guardando: false,
            tabs: [
                { key: "basic", label: "Datos básicos" },
                { key: "icon", label: "Icono" },
            ],
            iconOptions: [],
        };
    },
    computed: {
        filteredModules() {
            if (!this.searchTerm) return this.modulesData;
            const term = this.searchTerm.toLowerCase();
            const filtered = [];
            for (const module of this.modulesData) {
                const matchInParent = module.titulo.toLowerCase().includes(term);
                const matchingChildren = module.children?.filter(child =>
                    child.titulo.toLowerCase().includes(term)
                ) || [];
                if (matchInParent || matchingChildren.length > 0) {
                    filtered.push({
                        ...module,
                        children: matchingChildren
                    });
                }
            }
            return filtered;
        },
        parentModules() {
            return this.modulesData.filter(m => !m.padre_id);
        },
        filteredIcons() {
            if (!this.iconSearch) return this.iconOptions;
            return this.iconOptions.filter(icon =>
                icon.name.toLowerCase().includes(this.iconSearch.toLowerCase())
            );
        }
    },
    mounted() {
        this.cargarModulos();
        this.cargarIconos();
    },
    methods: {
        async cargarModulos() {
            this.loading = true;
            try {
                const response = await list_menu();
                this.modulesData = response.data || [];
            } catch (error) {
                console.error("Error cargando módulos:", error);
                sweetalert2.fire("Error", "No se pudieron cargar los módulos", "error");
            } finally {
                this.loading = false;
            }
        },

        cargarIconos() {
            this.iconOptions = Object.keys(Icons).map(name => ({
                name,
                component: Icons[name],
                label: name.replace('Icon', '')
            }));
        },

        getIconComponent(iconName) {
            return Icons[iconName] || Icons.FolderIcon;
        },

        toggleExpand(id) {
            this.expandedState = {
                ...this.expandedState,
                [id]: !this.expandedState[id]
            };
        },

        expandAll() {
            const newState = {};
            this.modulesData.forEach(m => {
                newState[m.id] = true;
            });
            this.expandedState = newState;
        },

        collapseAll() {
            this.expandedState = {};
        },

        async openModal(module) {
            if (module) {
                this.selectedModule = { ...module };
            } else {
                this.selectedModule = {
                    titulo: "",
                    ruta: null,
                    icono: "ListBulletIcon",
                    orden: 0,
                    activo: true,
                    padre_id: null,
                };
            }
            this.activeTab = "basic";
            this.iconSearch = "";
            this.errors = {};
            this.showModal = true;
        },

        btnCerrarModal() {
            this.showModal = false;
            this.selectedModule = {
                titulo: "",
                ruta: null,
                icono: "ListBulletIcon",
                orden: 0,
                activo: true,
                padre_id: null,
            };
            this.errors = {};
        },

        validarFormulario() {
            this.errors = {};

            if (!this.selectedModule.titulo || this.selectedModule.titulo.trim() === "") {
                this.errors.titulo = "El título del módulo es requerido";
            }

            if (this.selectedModule.orden < 0) {
                this.errors.orden = "El orden no puede ser negativo";
            }

            return Object.keys(this.errors).length === 0;
        },

        async btnConfirmar() {
            if (!this.validarFormulario()) {
                return;
            }

            this.guardando = true;
            const data = {
                id: this.selectedModule.id,
                menu_titulo: this.selectedModule.titulo,
                menu_ruta: this.selectedModule.ruta,
                menu_icono: this.selectedModule.icono,
                menu_orden: this.selectedModule.orden || 0,
                menu_activo: this.selectedModule.activo,
                menu_padre_id: this.selectedModule.padre_id,
            };

            try {
                await save_menu(data);
                await this.cargarModulos();
                this.btnCerrarModal();
                sweetalert2.fire("Éxito", "Módulo guardado correctamente", "success");
            } catch (error) {
                console.error("Error al guardar módulo:", error);
                sweetalert2.fire("Error", "No se pudo guardar el módulo", "error");
            } finally {
                this.guardando = false;
            }
        },

        confirmDelete(module) {
            this.moduleAEliminar = module;
            this.showDeleteModal = true;
        },

        async eliminarModulo() {
            if (this.moduleAEliminar) {
                try {
                    // await delete_menu(this.moduleAEliminar.id);
                    sweetalert2.fire("Éxito", "Módulo eliminado correctamente", "success");
                    await this.cargarModulos();
                } catch (error) {
                    console.error("Error eliminando módulo:", error);
                    sweetalert2.fire("Error", "No se pudo eliminar el módulo", "error");
                } finally {
                    this.showDeleteModal = false;
                    this.moduleAEliminar = null;
                }
            }
        },
    },
};
</script>