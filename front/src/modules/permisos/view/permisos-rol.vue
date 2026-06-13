<template>
    <div class="bg-gray-50 flex flex-col">
        <!-- Header -->
        <div class="bg-white border-b border-gray-200 px-4 md:px-6 py-4 sticky top-0 z-10">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                <div>
                    <h1 class="text-lg md:text-xl font-semibold text-gray-800">
                        Gestión de Roles
                    </h1>
                    <p class="text-xs md:text-xs text-gray-500 mt-0.5">
                        Administración de permisos y accesos al sistema
                    </p>
                </div>

                <button @click="openModal(null)"
                    class="w-full md:w-auto inline-flex justify-center items-center gap-2 px-4 py-2 bg-gray-900 hover:bg-gray-900 text-white text-xs font-medium rounded-lg shadow-xs transition-all duration-200">Nuevo Rol
                </button>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex-1 flex items-center justify-center py-12">
            <div class="text-center">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <p class="mt-2 text-gray-500">Cargando roles...</p>
            </div>
        </div>

        <!-- Tabla -->
        <div v-else class="flex-1 px-4 md:px-6 py-4 md:py-6">
            <div class="bg-white rounded-xl border border-gray-200 shadow-xs overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="min-w-[700px] w-full">
                        <thead class="bg-gray-50 border-b border-gray-200">
                            <tr>
                                <th
                                    class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600  tracking-wider">
                                    Rol
                                </th>
                                <th
                                    class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600  tracking-wider">
                                    Descripción
                                </th>
                                <th
                                    class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600  tracking-wider">
                                    Estado
                                </th>
                                <th
                                    class="px-4 md:px-6 py-4 text-center text-xs font-semibold text-gray-600  tracking-wider">
                                    Acciones
                                </th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            <tr v-for="role in roles" :key="role.id" class="hover:bg-gray-50 transition-colors">
                                <td class="px-4 md:px-6 py-4 whitespace-nowrap">
                                    <div class="flex items-center gap-2 md:gap-3">
                                        <span class="text-xs font-medium text-gray-900">
                                            {{ role.rol_nombre }}
                                        </span>
                                    </div>
                                </td>
                                <td class="px-4 md:px-6 py-4">
                                    <span class="text-xs text-gray-600 line-clamp-1">
                                        {{ role.rol_descripcion || "Sin descripción" }}
                                    </span>
                                </td>
                                <td class="px-4 md:px-6 py-4 whitespace-nowrap">
                                    <span :class="role.rol_activo
                                            ? 'bg-green-100 text-green-800'
                                            : 'bg-gray-100 text-gray-600'
                                        " class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium">
                                        <span :class="role.rol_activo ? 'bg-green-500' : 'bg-gray-400'"
                                            class="w-1.5 h-1.5 rounded-full"></span>
                                        {{ role.rol_activo ? "Activo" : "Inactivo" }}
                                    </span>
                                </td>
                                <td class="px-4 md:px-6 py-4 text-center">
                                    <div class="flex justify-center gap-2">
                                        <button @click="openModal(role)"
                                            class="text-xs font-medium text-gray-600 hover:text-blue-600 px-3 py-1.5 rounded-md hover:bg-blue-50 transition-all">
                                            Editar
                                        </button>
                                        <button @click="confirmDelete(role)"
                                            class="text-xs font-medium text-gray-600 hover:text-red-600 px-3 py-1.5 rounded-md hover:bg-red-50 transition-all">
                                            Eliminar
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            <tr v-if="roles && roles.length === 0">
                                <td colspan="4" class="px-6 py-12 text-center text-gray-500">
                                    No se encontraron roles
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Modal mejorado -->
        <div v-if="showModal" class="fixed inset-0 z-50 overflow-y-auto">
            <div class="fixed inset-0 bg-black/50 backdrop-blur-xs" @click="btnCerrarModal"></div>

            <div class="flex min-h-full items-center justify-center p-4">
                <div class="relative bg-white w-full max-w-2xl rounded-xl shadow-2xl flex flex-col max-h-[90vh]">
                    <!-- Header mejorado -->
                    <div
                        class="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-white rounded-t-xl">
                        <div>
                            <h3 class="text-lg font-semibold text-gray-800">
                                {{ selectedRole?.id ? "Actualizar Rol" : "Crear Nuevo Rol" }}
                            </h3>
                            <p class="text-xs text-gray-500">
                                {{
                                    selectedRole?.id
                                        ? "Modifica la configuración del rol"
                                        : "Ingresa los datos del nuevo rol"
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
                                            Nombre del rol <span class="text-red-500">*</span>
                                        </label>
                                        <input v-model="selectedRole.rol_nombre" type="text"
                                            class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                                            placeholder="Ej: Administrador" />
                                        <p v-if="errors.rol_nombre" class="text-xs text-red-500 mt-1">{{ errors.rol_nombre }}</p>
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-gray-700 mb-1">
                                            Estado
                                        </label>
                                        <select v-model="selectedRole.rol_activo"
                                            class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white">
                                            <option :value="true">Activo</option>
                                            <option :value="false">Inactivo</option>
                                        </select>
                                    </div>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-gray-700 mb-1">
                                        Descripción
                                    </label>
                                    <textarea v-model="selectedRole.rol_descripcion" rows="3"
                                        class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                                        placeholder="Describe las responsabilidades y alcance del rol..."></textarea>
                                </div>
                            </div>

                            <!-- Tab: Permisos y accesos mejorada -->
                            <div v-show="activeTab === 'permissions'" class="space-y-4">
                                <!-- Barra de herramientas -->
                                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                                    <div class="flex items-center gap-2">
                                        <button @click="expandAll"
                                            class="text-xs text-blue-600 hover:text-blue-700 px-2 py-1 rounded hover:bg-blue-50">
                                            Expandir todo
                                        </button>
                                        <span class="text-gray-300">|</span>
                                        <button @click="collapseAll"
                                            class="text-xs text-blue-600 hover:text-blue-700 px-2 py-1 rounded hover:bg-blue-50">
                                            Colapsar todo
                                        </button>
                                        <span class="text-gray-300">|</span>
                                        <button @click="selectAll"
                                            class="text-xs text-blue-600 hover:text-blue-700 px-2 py-1 rounded hover:bg-blue-50">
                                            Seleccionar todo
                                        </button>
                                        <span class="text-gray-300">|</span>
                                        <button @click="clearAll"
                                            class="text-xs text-red-600 hover:text-red-700 px-2 py-1 rounded hover:bg-red-50">
                                            Limpiar todo
                                        </button>
                                    </div>
                                </div>

                                <div
                                    class="border border-gray-200 rounded-md overflow-hidden max-h-72 sm:max-h-80 overflow-y-auto">
                                    <div v-for="menu in menus" :key="menu.id"
                                        class="border-b border-gray-100 last:border-0">
                                        <!-- Menú padre -->
                                        <div class="flex items-center gap-3 px-3 sm:px-4 py-2.5 hover:bg-gray-50">
                                            <!-- Botón expandir/colapsar -->
                                            <button v-if="menu.children?.length" @click="toggleExpand(menu)"
                                                class="text-gray-500 hover:text-gray-700 transition-transform"
                                                :class="{ 'rotate-90': menu.expanded }">
                                                <component :is="Icons.ChevronRightIcon" class="w-4 h-4" />
                                            </button>
                                            <div v-else class="w-4"></div>

                                            <!-- Checkbox padre con soporte para estado indeterminado -->
                                            <label class="flex items-center gap-3 cursor-pointer flex-1">
                                                <input 
                                                    type="checkbox" 
                                                    :checked="menu.checked"
                                                    :indeterminate.prop="menu.indeterminate"
                                                    @change="toggleChildren(menu, $event)"
                                                    class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-2 focus:ring-blue-500" 
                                                />
                                                <span class="text-xs font-medium text-gray-800">
                                                    {{ menu.titulo }}
                                                </span>
                                            </label>
                                        </div>

                                        <!-- Submenús -->
                                        <div v-if="menu.children?.length && menu.expanded"
                                            class="pl-9 sm:pl-11 pr-3 sm:pr-4 pb-2 relative">
                                            <!-- Línea vertical guía -->
                                            <div class="absolute left-5 top-0 w-px h-[65px] bg-gray-300"></div>

                                            <div v-for="child in menu.children" :key="child.id"
                                                class="relative flex items-center gap-3 py-1.5">
                                                <!-- Línea horizontal de conexión -->
                                                <div class="absolute left-1 top-1/2 w-4 h-px bg-gray-300"></div>

                                                <label class="flex items-center gap-3 cursor-pointer pl-6">
                                                    <input 
                                                        type="checkbox" 
                                                        v-model="child.checked"
                                                        @change="checkParent(menu)"
                                                        class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-2 focus:ring-blue-500" 
                                                    />
                                                    <span class="text-xs text-gray-600">
                                                        {{ child.titulo }}
                                                    </span>
                                                </label>
                                            </div>
                                        </div>
                                    </div>
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
                            {{ guardando ? 'Guardando...' : (selectedRole?.id ? "Actualizar" : "Crear") }}
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
                            ¿Estás seguro de que deseas eliminar el rol "{{ roleAEliminar?.rol_nombre }}"?<br>
                            Esta acción no se puede deshacer.
                        </p>
                        <div class="flex gap-3">
                            <button @click="showDeleteModal = false"
                                class="flex-1 px-4 py-2 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
                                Cancelar
                            </button>
                            <button @click="eliminarRol"
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
import { 
    list_rol, 
    list_rol_x_menu, 
    save_rol
    // delete_rol
} from "../api/permisos-rol.ts";
import sweetalert2 from "sweetalert2";
import * as Icons from "@heroicons/vue/24/outline";

export default {
    name: "GestionRoles",
    data() {
        return {
            Icons,
            roles: [],
            selectedRole: {
                rol_nombre: "",
                rol_descripcion: "",
                rol_activo: true,
            },
            menus: [],
            showModal: false,
            showDeleteModal: false,
            roleAEliminar: null,
            activeTab: "basic",
            searchTerm: "",
            errors: {},
            loading: false,
            guardando: false,
            tabs: [
                { key: "basic", label: "Información básica" },
                { key: "permissions", label: "Permisos y accesos" },
            ],
        };
    },
    mounted() {
        this.cargarRoles();
    },
    methods: {
        async cargarRoles() {
            this.loading = true;
            try {
                const response = await list_rol();
                this.roles = response.data || [];
            } catch (error) {
                console.error("Error cargando roles:", error);
                sweetalert2.fire("Error", "No se pudieron cargar los roles", "error");
            } finally {
                this.loading = false;
            }
        },

        getSelectedMenus() {
            const selected = [];
            
            this.menus.forEach((menu) => {
                if (menu.checked || menu.indeterminate) {
                    selected.push(menu.id);
                }
                if (menu.children) {
                    menu.children.forEach((c) => {
                        if (c.checked) {
                            selected.push(c.id);
                        }
                    });
                }
            });
            return selected;
        },

        expandAll() {
            this.menus.forEach((menu) => {
                if (menu.children?.length) menu.expanded = true;
            });
        },

        collapseAll() {
            this.menus.forEach((menu) => {
                menu.expanded = false;
            });
        },

        selectAll() {
            this.menus.forEach((menu) => {
                menu.checked = true;
                menu.indeterminate = false;
                if (menu.children) {
                    menu.children.forEach((c) => (c.checked = true));
                }
            });
        },

        clearAll() {
            this.menus.forEach((menu) => {
                menu.checked = false;
                menu.indeterminate = false;
                if (menu.children) {
                    menu.children.forEach((c) => (c.checked = false));
                }
            });
        },

        toggleExpand(menu) {
            menu.expanded = !menu.expanded;
        },

        toggleChildren(menu, event) {
            if (menu.children) {
                const nuevoEstado = event.target.checked;
                menu.children.forEach((c) => {
                    c.checked = nuevoEstado;
                });
                menu.indeterminate = false;
                menu.checked = nuevoEstado;
            }
        },

        checkParent(menu) {
            if (!menu.children) return;
            
            const allChecked = menu.children.every((c) => c.checked);
            const someChecked = menu.children.some((c) => c.checked);
            
            if (allChecked) {
                menu.checked = true;
                menu.indeterminate = false;
            } else if (someChecked) {
                menu.checked = false;
                menu.indeterminate = true;
            } else {
                menu.checked = false;
                menu.indeterminate = false;
            }
        },

        async openModal(role) {
            if (role) {
                this.guardando = true;
                this.selectedRole = { ...role };
            } else {
                this.selectedRole = {
                    rol_nombre: "",
                    rol_descripcion: "",
                    rol_activo: true,
                };
            }
            
            this.showModal = true;
            this.activeTab = "basic";
            this.searchTerm = "";
            this.errors = {};

            try {
                const response = await list_rol_x_menu(role?.id || 0);
                this.menus = response.data.map((m) => ({
                    ...m,
                    expanded: false,
                    indeterminate: false,
                    checked: m.checked || false,
                    children: m.children?.map((c) => ({
                        ...c,
                        checked: c.checked || false,
                    })),
                }));
                
                this.menus.forEach((menu) => {
                    if (menu.children && menu.children.length > 0) {
                        this.checkParent(menu);
                    }
                });
            } catch (error) {
                console.error("Error al cargar menús:", error);
                sweetalert2.fire("Error", "No se pudieron cargar los permisos", "error");
            } finally {
                this.guardando = false;
            }
        },

        btnCerrarModal() {
            this.showModal = false;
            this.selectedRole = {
                rol_nombre: "",
                rol_descripcion: "",
                rol_activo: true,
            };
            this.menus = [];
            this.errors = {};
        },

        validarFormulario() {
            this.errors = {};

            if (!this.selectedRole.rol_nombre || this.selectedRole.rol_nombre.trim() === "") {
                this.errors.rol_nombre = "El nombre del rol es requerido";
            }

            return Object.keys(this.errors).length === 0;
        },

        async btnConfirmar() {
            if (!this.validarFormulario()) {
                return;
            }

            this.guardando = true;
            const data = {
                rol: this.selectedRole,
                menus: this.getSelectedMenus(),
            };

            try {
                await save_rol(data);
                await this.cargarRoles();
                this.btnCerrarModal();
                sweetalert2.fire("Éxito", "Rol guardado correctamente", "success");
            } catch (error) {
                console.error("Error al guardar rol:", error);
                sweetalert2.fire("Error", "No se pudo guardar el rol", "error");
            } finally {
                this.guardando = false;
            }
        },

        confirmDelete(role) {
            this.roleAEliminar = role;
            this.showDeleteModal = true;
        },

        async eliminarRol() {
            if (this.roleAEliminar) {
                try {
                    // await delete_rol(this.roleAEliminar.id);
                    // sweetalert2.fire("Éxito", "Rol eliminado correctamente", "success");
                    await this.cargarRoles();
                } catch (error) {
                    console.error("Error eliminando rol:", error);
                    sweetalert2.fire("Error", "No se pudo eliminar el rol", "error");
                } finally {
                    this.showDeleteModal = false;
                    this.roleAEliminar = null;
                }
            }
        },
    },
};
</script>