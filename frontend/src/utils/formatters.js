/**
 * Intent dictionary label mapping and helper formatters
 */

const INTENT_LABELS = {
  order_not_received: "Order Not Received",
  delivery_delay: "Delivery Delay",
  delivery_tracking: "Tracking & Status",
  delivery_attempt_issue: "Delivery Attempt Issue",
  wrong_or_missing_item: "Wrong / Missing Item",
  damaged_product: "Damaged / Defective Product",
  return_issue: "Returns & Pickup",
  refund_issue: "Refund Status",
  order_cancellation: "Order Cancellation",
  payment_issue: "Billing & Payment",
  account_issue: "Account & Security",
  seller_issue: "Third-Party Seller",
  product_information: "Product Information",
  stock_availability: "Stock Availability",
  digital_or_app_issue: "Prime & Digital Services",
  customer_support_issue: "Support Escalation",
  shipping_or_delivery_question: "Shipping Policy",
  other: "General Inquiries",
};

/**
 * Converts snake_case intent to formatted title
 * @param {string} intent
 * @returns {string}
 */
export function formatIntent(intent) {
  if (!intent) return "General Support";
  if (INTENT_LABELS[intent]) return INTENT_LABELS[intent];
  
  // Format snake_case to Title Case as fallback
  return intent
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

/**
 * Returns user-friendly decision metadata
 * @param {string} decision
 */
export function formatDecision(decision) {
  const norm = (decision || '').toUpperCase();
  const isEscalation = norm.includes('ESCALATE') || norm.includes('HUMAN');
  return {
    isEscalation,
    title: isEscalation ? "Requires escalation" : "Automatically handled",
    badgeClass: isEscalation ? "decision-escalate" : "decision-autohandle",
    icon: isEscalation ? "alert" : "check",
  };
}

/**
 * Formats date/timestamp for message bubble
 * @param {string|number|Date} date
 * @returns {string}
 */
export function formatMessageTime(date) {
  const d = date ? new Date(date) : new Date();
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
