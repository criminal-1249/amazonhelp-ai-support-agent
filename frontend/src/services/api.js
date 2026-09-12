/**
 * Dedicated API Service for Amazon Help AI Support Agent
 * Connects to FastAPI backend through Vercel proxy
 */

const rawBase = import.meta.env.VITE_API_URL;
const API_BASE_URL = (
  rawBase && typeof rawBase === "string" && rawBase.trim().length > 0
    ? rawBase.trim()
    : "/api"
).replace(/\/+$/, "");

/**
 * Checks backend health status through Vercel proxy (/api/)
 * Includes a lightweight retry (1 retry) on timeout or network error to avoid false offline alerts
 */
export async function checkBackendHealth(retries = 1) {
  const url = `${API_BASE_URL}/`;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 6000);

      const response = await fetch(url, {
        method: "GET",
        headers: {
          Accept: "application/json",
          "Cache-Control": "no-cache",
          Pragma: "no-cache",
        },
        cache: "no-store",
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      // Successful HTTP 200 -> Agent Online
      if (response.ok) {
        let data = null;
        try {
          data = await response.json();
        } catch (_) {
          data = { status: "running" };
        }
        return {
          ok: true,
          status: response.status,
          data,
        };
      }

      // If backend returned an HTTP error (e.g. 500, 502, 503), retry once
      if (attempt < retries) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        continue;
      }

      return {
        ok: false,
        status: response.status,
        error: `HTTP ${response.status}`,
      };
    } catch (err) {
      if (attempt < retries) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        continue;
      }

      return {
        ok: false,
        status: null,
        error:
          err.name === "AbortError"
            ? "Connection timed out"
            : "Backend offline",
      };
    }
  }

  return { ok: false, error: "Backend offline" };
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