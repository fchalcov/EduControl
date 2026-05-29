<template>
    <div class="bg-gray-50 flex flex-col">
        <!-- Header -->
        <div class="bg-white border-b border-gray-200 px-4 md:px-6 py-4 sticky top-0 z-10">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                <div>
                    <h1 class="text-lg md:text-xl font-semibold text-gray-800">
                        Gestión de Roles
                    </h1>
                    <p class="text-xs md:text-sm text-gray-500 mt-0.5">
                        Administración de permisos y accesos al sistema
                    </p>
                </div>

                <button @click="openModal(null)"
                    class="w-full md:w-auto inline-flex justify-center items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg shadow-sm transition-all duration-200">
                    Nuevo Rol
                </button>
            </div>
        </div>

        <!-- Tabla -->
        <div class="flex-1 px-4 md:px-6 py-4 md:py-6">
            <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="min-w-[700px] w-full">
                        <thead class="bg-gray-50 border-b border-gray-200">
                            <tr>
                                <th
                                    class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Rol
                                </th>
                                <th
                                    class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Descripción
                                </th>
                                <th
                                    class="px-4 md:px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Estado
                                </th>
                                <th
                                    class="px-4 md:px-6 py-4 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Acciones
                                </th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            <tr v-for="role in roles" :key="role.id" class="hover:bg-gray-50 transition-colors">
                                <td class="px-4 md:px-6 py-4 whitespace-nowrap">
                                    <div class="flex items-center gap-2 md:gap-3">
                                        <span class="text-sm font-medium text-gray-900">
                                            {{ role.rol_nombre }}
                                        </span>
                                    </div>
                                </td>
                                <td class="px-4 md:px-6 py-4">
                                    <span class="text-sm text-gray-600 line-clamp-1">
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
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Modal mejorado -->
        <div v-if="showModal" class="fixed inset-0 z-50 overflow-y-auto">
            <div class="fixed inset-0 bg-black/50 backdrop-blur-sm" @click="btnCerrarModal"></div>

            <div class="flex min-h-full items-center justify-center p-4">
                <div class="relative bg-white w-full max-w-2xl rounded-xl shadow-2xl flex flex-col max-h-[90vh]">
                    <!-- Header mejorado -->
                    <div
                        class="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-white rounded-t-xl">
                        <div>
                            <h3 class="text-lg font-semibold text-gray-800">
                                {{ selectedRole?.id ? "Actualizar Rol" : "Crear Nuevo Rol" }}
                            </h3>
                            <p class="text-sm text-gray-500">
                                {{
                                    selectedRole?.id
                                        ? "Modifica la configuración del rol"
                                        : "Ingresa los datos del nuevo rol"
                                }}
                            </p>
                        </div>
                        <button @click="btnCerrarModal"
                            class="text-gray-400 hover:text-gray-600 transition-colors p-1 rounded-lg hover:bg-gray-100">
                            ×
                        </button>
                    </div>

                    <!-- Body con tabs -->
                    <div class="flex-1 overflow-hidden flex flex-col">
                        <!-- Tabs de navegación -->
                        <div class="border-b border-gray-200 px-6">
                            <div class="flex gap-6 overflow-x-auto">
                                <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key" :class="[
                                    'py-3 text-sm font-medium transition-colors relative whitespace-nowrap',
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
                                        <label class="block text-sm font-medium text-gray-700 mb-1">
                                            Nombre del rol <span class="text-red-500">*</span>
                                        </label>
                                        <input v-model="selectedRole.rol_nombre" type="text"
                                            class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                                            placeholder="Ej: Administrador" />
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">
                                            Estado
                                        </label>
                                        <select v-model="selectedRole.rol_activo"
                                            class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white">
                                            <option :value="true">Activo</option>
                                            <option :value="false">Inactivo</option>
                                        </select>
                                    </div>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">
                                        Descripción
                                    </label>
                                    <textarea v-model="selectedRole.rol_descripcion" rows="3"
                                        class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
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
                                                    :indeterminate="menu.indeterminate"
                                                    @change="toggleChildren(menu , $event)"
                                                    class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-2 focus:ring-blue-500" 
                                                />
                                                <span class="text-sm font-medium text-gray-800">
                                                    {{ menu.titulo }}
                                                </span>
                                            </label>
                                        </div>

                                        <!-- Submenús -->
                                        <transition name="fade">
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
                                                        <span class="text-sm text-gray-600">
                                                            {{ child.titulo }}
                                                        </span>
                                                    </label>
                                                </div>
                                            </div>
                                        </transition>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Footer mejorado -->
                    <div
                        class="flex flex-col sm:flex-row justify-end gap-3 px-6 py-4 border-t border-gray-200 bg-gray-50 rounded-b-xl">
                        <button @click="btnCerrarModal"
                            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                            Cancelar
                        </button>
                        <button @click="btnConfirmar"
                            class="px-6 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors shadow-sm">
                            {{ selectedRole?.id ? "Actualizar" : "Crear" }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { list_rol, list_rol_x_menu, save_rol } from "../api/permisos-rol.ts";
import sweetalert2 from "sweetalert2";
import * as Icons from "@heroicons/vue/24/outline";

// Estado
const roles = ref<any[]>([]);
const showModal = ref(false);
const selectedRole = ref<any>(null);
const menus = ref<any[]>([]);
const activeTab = ref("basic");
const searchTerm = ref("");

// Tabs
const tabs = [
    { key: "basic", label: "Información básica" },
    { key: "permissions", label: "Permisos y accesos" },
];

const getSelectedMenus = () => {
    const selected: number[] = [];
    
    menus.value.forEach((menu: any) => {
        if (menu.checked || menu.indeterminate) {
            selected.push(menu.id);
        }
        if (menu.children) {
            menu.children.forEach((c: any) => {
                if (c.checked) {
                    selected.push(c.id);
                }
            });
        }
    });
    return selected;
};

// Expandir/colapsar todo
const expandAll = () => {
    menus.value.forEach((menu) => {
        if (menu.children?.length) menu.expanded = true;
    });
};

const collapseAll = () => {
    menus.value.forEach((menu) => {
        menu.expanded = false;
    });
};

// Seleccionar/limpiar todo
const selectAll = () => {
    menus.value.forEach((menu) => {
        menu.checked = true;
        menu.indeterminate = false;
        if (menu.children) {
            menu.children.forEach((c: any) => (c.checked = true));
        }
    });
};

const clearAll = () => {
    menus.value.forEach((menu) => {
        menu.checked = false;
        menu.indeterminate = false;
        if (menu.children) {
            menu.children.forEach((c: any) => (c.checked = false));
        }
    });
};

// Toggle expandir menú
const toggleExpand = (menu: any) => {
    menu.expanded = !menu.expanded;
};

// Toggle hijos cuando se selecciona padre
const toggleChildren = (menu: any, event: any) => {
    if (menu.children) {
        const nuevoEstado = event.target.checked;  // Obtener el nuevo estado
        menu.children.forEach((c: any) => {
            c.checked = nuevoEstado;  // Usar el nuevo estado
        });
        menu.indeterminate = false;
        menu.checked = nuevoEstado;  // Asegurar que el padre tiene el estado correcto
    }
};
// Verificar padre cuando se selecciona hijo
const checkParent = (menu: any) => {
    if (!menu.children) return;
    
    const allChecked = menu.children.every((c: any) => c.checked);
    const someChecked = menu.children.some((c: any) => c.checked);
    
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
};

const rs_list = async () => {
    try {
        const response = await list_rol();
        roles.value = response.data;
    } catch (error) {
        sweetalert2.fire("Error", "No se pudieron cargar los roles", "error");
    }
};

const openModal = async (role: any) => {
    selectedRole.value = role
        ? { ...role }
        : {
            rol_nombre: "",
            rol_descripcion: "",
            rol_activo: true,
        };
    showModal.value = true;
    activeTab.value = "basic";
    searchTerm.value = "";

    try {
        const response = await list_rol_x_menu(role?.id || 0);
        menus.value = response.data.map((m: any) => ({
            ...m,
            expanded: false,
            indeterminate: false,
            checked: m.checked || false,
            children: m.children?.map((c: any) => ({
                ...c,
                checked: c.checked || false,
            })),
        }));
        
        // Después de cargar los menús, verificar el estado de cada padre
        menus.value.forEach((menu: any) => {
            if (menu.children && menu.children.length > 0) {
                checkParent(menu);
            }
        });
    } catch (error) {
        console.error("Error al cargar menús:", error);
        sweetalert2.fire("Error", "No se pudieron cargar los permisos", "error");
    }
};

const confirmDelete = (role: any) => {
    sweetalert2
        .fire({
            title: "¿Estás seguro?",
            text: `¿Deseas eliminar el rol "${role.rol_nombre}"? Esta acción no se puede deshacer.`,
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
            confirmButtonText: "Sí, eliminar",
            cancelButtonText: "Cancelar",
        })
        .then((result) => {
            if (result.isConfirmed) {
                // Aquí iría la lógica para eliminar el rol
                sweetalert2.fire(
                    "Eliminado",
                    `El rol "${role.rol_nombre}" ha sido eliminado.`,
                    "success",
                );
            }
        });
};

const btnCerrarModal = () => {
    showModal.value = false;
    selectedRole.value = null;
    menus.value = [];
    searchTerm.value = "";
};

const btnConfirmar = async () => {
    if (!selectedRole.value.rol_nombre?.trim()) {
        sweetalert2.fire("Error", "El nombre del rol es obligatorio", "error");
        return;
    }

    const data = {
        rol: selectedRole.value,
        menus: getSelectedMenus(),
    };

    try {
        await save_rol(data);
        await rs_list();
        btnCerrarModal();
        sweetalert2.fire("Éxito", "Rol guardado correctamente", "success");
    } catch (error) {
        console.error("Error al guardar rol:", error);
        sweetalert2.fire("Error", "No se pudo guardar el rol", "error");
    }
};

onMounted(() => {
    rs_list();
});
</script>