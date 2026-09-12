/**
 * Dedicated API Service for Amazon Help AI Support Agent
 * Connects to FastAPI backend (/chat and /)
 */

// Fallback to local FastAPI address if environment variable is not defined
const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/+$/, '');

/**
 * Checks backend health status
 * @returns {Promise<{ ok: boolean, data?: any, error?: string }>}
 */
export async function checkBackendHealth() {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000);

    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (response.ok) {
      const data = await response.json();
      return { ok: true, data };
    }
    return { ok: false, error: `HTTP ${response.status}` };
  } catch (err) {
    return {
      ok: false,
      error: err.name === 'AbortError' ? 'Connection timed out' : 'Backend offline',
    };
  }
}

/**
 * Sends customer message to the FastAPI /chat endpoint.
 * Note: Message is passed as a query parameter as required by the backend API contract.
 *
 * @param {string} message - Customer inquiry text
 * @returns {Promise<{
 *   customer_message: string,
 *   intent: string,
 *   response: string,
 *   decision: string,
 *   reason: string,
 *   evidence: Array<{customer_query: string, agent_reply: string, conversation_id: number|string}>
 * }>}
 */
export async function sendChatMessage(message) {
  if (!message || !message.trim()) {
    throw new Error('Message cannot be empty.');
  }

  const trimmed = message.trim();
  const endpoint = `${API_BASE_URL}/chat?message=${encodeURIComponent(trimmed)}`;

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 422) {
        throw new Error("Unable to process this inquiry format. Please rephrase your message.");
      } else if (response.status === 500) {
        throw new Error("The support server encountered an internal issue. Please try again in a moment.");
      } else {
        throw new Error(`Support service returned error (HTTP ${response.status}). Please try again.`);
      }
    }

    const text = await response.text();
    if (!text) {
      throw new Error("Received empty response from support agent.");
    }

    let data;
    try {
      data = JSON.parse(text);
    } catch {
      throw new Error("Invalid response format received from support agent.");
    }

    // Validate expected structure with graceful fallbacks
    return {
      customer_message: data.customer_message || trimmed,
      intent: data.intent || 'general_support',
      response: data.response || "I am currently reviewing your inquiry. Please allow a moment.",
      decision: data.decision || 'AUTO_HANDLE',
      reason: data.reason || 'Processed standard customer inquiry.',
      evidence: Array.isArray(data.evidence) ? data.evidence : [],
    };
  } catch (err) {
    // Distinguish network/connection errors from thrown user errors
    if (err.name === 'TypeError' && err.message.includes('fetch')) {
      throw new Error("Sorry, I'm having trouble connecting to the support agent. Please make sure the backend server is running.");
    }
    throw err;
  }
}
