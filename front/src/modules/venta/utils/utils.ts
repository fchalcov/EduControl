// utils/pos-utils.ts
import Swal from 'sweetalert2';

// ==================== CONSTANTES Y CÓDIGOS ====================

export const PAYMENT_CODES = {
  CASH: 1,      // Efectivo
  YAPE: 2,      // Yape
} as const;

export const PAYMENT_LABELS = {
  [PAYMENT_CODES.CASH]: 'Efectivo',
  [PAYMENT_CODES.YAPE]: 'Yape',
} as const;

export const PAYMENT_ICONS = {
  [PAYMENT_CODES.CASH]: '',
  [PAYMENT_CODES.YAPE]: '',
} as const;

export const PAYMENT_COLORS = {
  [PAYMENT_CODES.CASH]: 'bg-gradient-to-r from-green-600 to-green-700',
  [PAYMENT_CODES.YAPE]: 'bg-gradient-to-r from-purple-600 to-purple-700',
} as const;

export const QUICK_CASH_AMOUNTS = [];

export const QUICK_BUTTON_LABELS = {
  PAY_ALL: 'Pagar todo',
  QUICK_AMOUNT: (amount: number) => `S/ ${amount}`,
};

// ==================== FORMATOS DE MONEDA Y NÚMEROS ====================

export const formatCurrency = (value: number | null | undefined): string => {
  if (!value && value !== 0) return "0.00";
  return new Intl.NumberFormat('es-PE', {
    style: 'currency',
    currency: 'PEN',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value).replace('PEN', 'S/');
};

export const formatNumberDisplay = (value: number | null | undefined): string => {
  if (!value && value !== 0) return "0.00";
  return new Intl.NumberFormat('es-PE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(parseFloat(value as any));
};

export const formatNumberExact = (value: number | null | undefined): string => {
  if (!value && value !== 0) return "0";
  const num = parseFloat(value as any);
  return num.toString();
};

export const roundToTwoDecimals = (value: number | null | undefined): number | null => {
  if (value === null || value === undefined || isNaN(value)) return null;
  return Math.round(value * 100) / 100;
};

export const sanitizeCurrencyInput = (value: string): string => {
  let cleaned = value.replace(/[^\d.-]/g, '');
  const parts = cleaned.split('.');
  if (parts.length > 2) {
    cleaned = parts[0] + '.' + parts.slice(1).join('');
  }
  return cleaned;
};

export const parseCurrencyInput = (value: string): number | null => {
  const sanitized = sanitizeCurrencyInput(value);
  const num = parseFloat(sanitized);
  return isNaN(num) ? null : num;
};

// ==================== TIPOS ====================

export interface Payment {
  method: number;
  amount: number;
  changeAmount: number;
  received?: number;
  date?: string;
}

export interface PaymentMethod {
  value: number;
  label: string;
  color: string;
  icon: string;
}

// ==================== CÁLCULOS DE PAGOS ====================

export interface PaymentCalculations {
  subtotal: number;
  igvTotal: number;
  total: number;
  totalPaid: number;
  remainingBalance: number;
  totalVuelto: number;
}

export const calculateTotals = (cart: any[]): PaymentCalculations => {
  const subtotal = cart.reduce((sum, item) => sum + (parseFloat(item.precio_unitario) * item.quantity), 0);
  const igvTotal = subtotal * 0.00;
  const total = subtotal * 1.00;
  
  return {
    subtotal,
    igvTotal,
    total,
    totalPaid: 0,
    remainingBalance: total,
    totalVuelto: 0
  };
};

export const updatePaymentCalculations = (
  totals: PaymentCalculations,
  payments: Payment[]
): PaymentCalculations => {
  const totalPaid = payments.reduce((sum, p) => sum + p.amount, 0);
  const remainingBalance = Math.max(0, Math.round((totals.total - totalPaid) * 100) / 100);
  const totalVuelto = payments
    .filter(p => p.method === PAYMENT_CODES.CASH && p.changeAmount)
    .reduce((sum, p) => sum + p.changeAmount, 0);
  
  return {
    ...totals,
    totalPaid,
    remainingBalance,
    totalVuelto
  };
};

// ==================== MANEJO DE PAGOS ====================

export const createYapePayment = (amount: number): Payment => {
  return {
    method: PAYMENT_CODES.YAPE,
    amount: roundToTwoDecimals(amount)!,
    changeAmount: 0,
    date: new Date().toLocaleTimeString()
  };
};

export const createEfectivoPayment = (
  amount: number,
  remainingBalance: number
): Payment => {
  let changeAmount = 0;
  let paymentAmount = amount;
  
  if (amount >= remainingBalance) {
    paymentAmount = remainingBalance;
    changeAmount = roundToTwoDecimals(amount - remainingBalance)!;
  }
  
  return {
    method: PAYMENT_CODES.CASH,
    amount: roundToTwoDecimals(paymentAmount)!,
    changeAmount,
    received: amount,
    date: new Date().toLocaleTimeString()
  };
};

// ==================== VALIDACIONES ====================

export const validateEfectivoPayment = (
  amount: number | null
): { valid: boolean; errorMessage?: string } => {
  if (!amount || amount <= 0) {
    return { valid: false, errorMessage: 'Ingrese un monto válido' };
  }
  
  return { valid: true };
};

// ==================== ALERTAS CON SWEETALERT2 NATURAL ====================

// Toast - Notificaciones rápidas
export const showToast = (message: string, type: 'success' | 'error' | 'info' | 'warning' = 'success') => {
  const Toast = Swal.mixin({
    toast: true,
    position: 'bottom-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
  });
  
  Toast.fire({
    icon: type,
    title: message
  });
};

// Alerta de error
export const showErrorAlert = (message: string, title: string = 'Error') => {
  Swal.fire({
    icon: 'error',
    title: title,
    text: message,
    confirmButtonText: 'OK'
  });
};

// Alerta de venta completada
export const showSaleCompletedAlert = (correlativo: string, total: number): Promise<any> => {
  return Swal.fire({
    icon: 'success',
    title: '¡Venta completada!',
    text: `Correlativo: ${correlativo}\nTotal: ${formatCurrency(total)}`,
    confirmButtonText: 'Aceptar'
  });
};

// Alerta de pago registrado
export const showPaymentCompletedAlert = (totalPaid: number, vuelto: number) => {
  let message = `Total pagado: ${formatCurrency(totalPaid)}`;
  if (vuelto > 0) {
    message += `\nVuelto: ${formatCurrency(vuelto)}`;
  }
  
  Swal.fire({
    icon: 'success',
    title: '¡Pago registrado!',
    text: message,
    confirmButtonText: 'Continuar',
    timer: 2000
  });
};

// Alerta de pago incompleto
export const showIncompletePaymentAlert = (remainingBalance: number) => {
  Swal.fire({
    icon: 'warning',
    title: 'Pago incompleto',
    text: `Falta saldo por pagar: ${formatCurrency(remainingBalance)}`,
    confirmButtonText: 'OK'
  });
};

// Alerta de error al registrar venta
export const showSaleErrorAlert = (errorMsg: string) => {
  Swal.fire({
    icon: 'error',
    title: 'Error al registrar la venta',
    text: errorMsg,
    confirmButtonText: 'Cerrar'
  });
};

// Alerta de producto inactivo
export const showProductInactiveAlert = (productName: string) => {
  Swal.fire({
    icon: 'error',
    title: 'Producto inactivo',
    text: `El producto "${productName}" está inactivo`,
    confirmButtonText: 'OK'
  });
};

// Alerta de stock insuficiente
export const showInsufficientStockAlert = (productName: string, maxStock: number) => {
  Swal.fire({
    icon: 'warning',
    title: 'Stock insuficiente',
    text: `${productName} - Stock máximo disponible: ${maxStock}.`,
    confirmButtonText: 'OK'
  });
};

// Alerta sin stock
export const showNoStockAlert = (productName: string) => {
  Swal.fire({
    icon: 'error',
    title: 'Sin stock',
    text: `El producto "${productName}" no tiene stock disponible`,
    confirmButtonText: 'OK'
  });
};

// Alerta carrito vacío
export const showEmptyCartAlert = () => {
  Swal.fire({
    icon: 'info',
    title: 'Carrito vacío',
    text: 'No hay productos en el carrito',
    confirmButtonText: 'OK'
  });
};

// Alerta monto inválido
export const showInvalidAmountAlert = () => {
  Swal.fire({
    icon: 'error',
    title: 'Monto inválido',
    text: 'Ingrese un monto válido mayor a cero',
    confirmButtonText: 'OK'
  });
};

// ==================== UTILIDADES ====================

export const getCurrentDateFormatted = (): string => {
  const date = new Date();
  return date.toLocaleDateString('es-PE', { 
    day: '2-digit', 
    month: 'short', 
    year: 'numeric' 
  });
};

export const playBeep = () => {
  try {
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    oscillator.frequency.value = 880;
    gainNode.gain.value = 0.1;
    oscillator.start();
    gainNode.gain.exponentialRampToValueAtTime(0.00001, audioContext.currentTime + 0.2);
    oscillator.stop(audioContext.currentTime + 0.2);
  } catch (err) {}
};

export const getPaymentLabel = (methodCode: number): string => {
  return PAYMENT_LABELS[methodCode as keyof typeof PAYMENT_LABELS] || 'Desconocido';
};