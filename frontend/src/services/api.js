/**
 * Dedicated API Service for Amazon Help AI Support Agent
 * Connects to FastAPI backend (/chat and /)
 */

const API_BASE_URL = (
  import.meta.env.VITE_API_URL || "http://54.206.87.123"
).replace(/\/+$/, "");

/**
 * Checks backend health status
 */
export async function checkBackendHealth() {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000);

    const response = await fetch(`${API_BASE_URL}/`, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (response.ok) {
      const data = await response.json();
      return { ok: true, data };
    }

    return {
      ok: false,
      error: `HTTP ${response.status}`,
    };
  } catch (err) {
    return {
      ok: false,
      error:
        err.name === "AbortError"
          ? "Connection timed out"
          : "Backend offline",
    };
  }
}

/**
 * Sends customer message to FastAPI /chat endpoint.
 */
export async function sendChatMessage(message) {
  if (!message || !message.trim()) {
    throw new Error("Message cannot be empty.");
  }

  const trimmed = message.trim();

  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        message: trimmed,
      }),
    });

    if (!response.ok) {
      if (response.status === 422) {
        throw new Error(
          "Unable to process this inquiry format. Please rephrase your message."
        );
      }

      if (response.status === 500) {
        throw new Error(
          "The support server encountered an internal issue. Please try again in a moment."
        );
      }

      throw new Error(
        `Support service returned error (HTTP ${response.status}). Please try again.`
      );
    }

    const data = await response.json();

    return {
      customer_message: data.customer_message || trimmed,
      intent: data.intent || "general_support",
      response:
        data.response ||
        "I am currently reviewing your inquiry. Please allow a moment.",
      decision: data.decision || "AUTO_HANDLE",
      reason: data.reason || "Processed standard customer inquiry.",
      evidence: Array.isArray(data.evidence) ? data.evidence : [],
    };
  } catch (err) {
    if (err instanceof TypeError) {
      throw new Error(
        "Sorry, I'm having trouble connecting to the support agent."
      );
    }

    throw err;
  }
}