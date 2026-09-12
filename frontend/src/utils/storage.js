/**
 * LocalStorage conversation persistence
 */

const STORAGE_KEY = 'amazon_help_ai_conversations_v1';
const ACTIVE_ID_KEY = 'amazon_help_ai_active_conv_id';

/**
 * Loads all saved conversations
 * @returns {Array<{ id: string, title: string, updatedAt: number, messages: Array }>}
 */
export function loadConversations() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (err) {
    console.error('Failed to load conversations from storage:', err);
    return [];
  }
}

/**
 * Saves conversations array to localStorage
 * @param {Array} conversations
 */
export function saveConversations(conversations) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
  } catch (err) {
    console.error('Failed to save conversations to storage:', err);
  }
}

/**
 * Gets active conversation ID
 */
export function getActiveConversationId() {
  return localStorage.getItem(ACTIVE_ID_KEY) || null;
}

/**
 * Sets active conversation ID
 */
export function setActiveConversationId(id) {
  if (id) {
    localStorage.setItem(ACTIVE_ID_KEY, id);
  } else {
    localStorage.removeItem(ACTIVE_ID_KEY);
  }
}
