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

export const MAX_YAPE_AMOUNT = 500;

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

export const getPaymentMethods = (): PaymentMethod[] => {
  return [
    { 
      value: PAYMENT_CODES.CASH, 
      label: PAYMENT_LABELS[PAYMENT_CODES.CASH], 
      color: PAYMENT_COLORS[PAYMENT_CODES.CASH], 
      icon: PAYMENT_ICONS[PAYMENT_CODES.CASH] 
    },
    { 
      value: PAYMENT_CODES.YAPE, 
      label: PAYMENT_LABELS[PAYMENT_CODES.YAPE], 
      color: PAYMENT_COLORS[PAYMENT_CODES.YAPE], 
      icon: PAYMENT_ICONS[PAYMENT_CODES.YAPE] 
    },
  ];
};

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

export const calculateCashDifference = (
  cashAmount: number | null,
  remainingBalance: number
): number => {
  const received = cashAmount || 0;
  if (received >= remainingBalance) {
    return Math.round((received - remainingBalance) * 100) / 100;
  }
  return Math.round((remainingBalance - received) * 100) / 100;
};

export const isCashPaymentComplete = (
  cashAmount: number | null,
  remainingBalance: number
): boolean => {
  const received = cashAmount || 0;
  return received >= remainingBalance;
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

export const validateYapePayment = (
  amount: number | null,
  remainingBalance: number,
  maxAmount: number
): { valid: boolean; errorMessage?: string } => {
  if (!amount || amount <= 0) {
    return { valid: false, errorMessage: 'Ingrese un monto válido' };
  }
  
  if (amount > remainingBalance) {
    return { valid: false, errorMessage: `El monto no puede exceder el saldo pendiente (${formatCurrency(remainingBalance)})` };
  }
  
  if (amount > maxAmount) {
    return { valid: false, errorMessage: `${PAYMENT_LABELS[PAYMENT_CODES.YAPE]} tiene un límite de ${formatCurrency(maxAmount)} por transacción` };
  }
  
  return { valid: true };
};

export const validateEfectivoPayment = (
  amount: number | null
): { valid: boolean; errorMessage?: string } => {
  if (!amount || amount <= 0) {
    return { valid: false, errorMessage: 'Ingrese un monto válido' };
  }
  
  return { valid: true };
};

// ==================== ALERTAS ====================

export const showToast = (message: string, type: 'success' | 'error' | 'info' | 'warning' = 'success') => {
  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
  });
  
  Toast.fire({
    icon: type,
    title: message
  });
};

export const showSuccessAlert = (message: string, title: string = '¡Éxito!') => {
  Swal.fire({
    icon: 'success',
    title: title,
    text: message,
    confirmButtonColor: '#1e293b',
    confirmButtonText: 'Aceptar',
    timer: 2500
  });
};

export const showErrorAlert = (message: string, title: string = 'Error') => {
  Swal.fire({
    icon: 'error',
    title: title,
    text: message,
    confirmButtonColor: '#1e293b',
    confirmButtonText: 'Entendido'
  });
};

export const showSaleCompletedAlert = (correlativo: string, total: number): Promise<any> => {
  return Swal.fire({
    icon: 'success',
    title: '✅ ¡Venta completada!',
    text: `Correlativo: ${correlativo}\nTotal: ${formatCurrency(total)}\n\n¡Gracias por su compra!`,
    confirmButtonColor: '#1e293b',
    confirmButtonText: 'Aceptar'
  });
};

export const showPaymentCompletedAlert = (totalPaid: number, vuelto: number) => {
  let message = `Total pagado: ${formatCurrency(totalPaid)}`;
  if (vuelto > 0) {
    message += `\nVuelto total: ${formatCurrency(vuelto)}`;
  }
  
  Swal.fire({
    icon: 'success',
    title: '¡Pago registrado!',
    text: message,
    confirmButtonColor: '#1e293b',
    confirmButtonText: 'Continuar',
    timer: 2000
  });
};

export const showIncompletePaymentAlert = (remainingBalance: number) => {
  showErrorAlert(`Falta saldo por pagar: ${formatCurrency(remainingBalance)}`, 'Pago incompleto');
};

export const showSaleErrorAlert = (errorMsg: string) => {
  showErrorAlert(errorMsg, 'Error al registrar la venta');
};

export const showProductInactiveAlert = (productName: string) => {
  showErrorAlert(`El producto "${productName}" está inactivo`, 'Producto inactivo');
};

export const showInsufficientStockAlert = (productName: string, maxStock: number) => {
  showErrorAlert(`Stock máximo disponible: ${maxStock} unidades`, `Stock insuficiente de "${productName}"`);
};

export const showNoStockAlert = (productName: string) => {
  showErrorAlert(`El producto "${productName}" no tiene stock disponible`, 'Sin stock');
};

export const showEmptyCartAlert = () => {
  showErrorAlert('El carrito está vacío', 'No hay productos');
};

export const showInvalidAmountAlert = () => {
  showErrorAlert('Ingrese un monto válido', 'Monto inválido');
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

export const getPaymentIcon = (methodCode: number): string => {
  return PAYMENT_ICONS[methodCode as keyof typeof PAYMENT_ICONS] || '💳';
};