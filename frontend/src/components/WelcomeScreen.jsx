import React from 'react';
import { Bot, ArrowRight } from 'lucide-react';

const SUGGESTED_PROMPTS = [
  "Where is my order?",
  "I received the wrong product",
  "I want to return my order",
  "My refund hasn't arrived",
  "I received a damaged product",
  "I am happy with this product"
];

export default function WelcomeScreen({ onSelectPrompt }) {
  return (
    <div className="welcome-container">
      <div className="welcome-icon-box">
        <Bot size={28} />
      </div>

      <h2 className="welcome-title">How can we help you today?</h2>
      <p className="welcome-description">
        Ask a question or describe an issue with your Amazon order. Our AI support agent will analyze your inquiry against verified historical resolutions and assist you immediately.
      </p>

      <div className="welcome-prompt-title">Ask about:</div>

      <div className="prompt-suggestions-grid">
        {SUGGESTED_PROMPTS.map((prompt, idx) => (
          <button
            key={idx}
            className="btn-prompt-suggestion"
            onClick={() => onSelectPrompt(prompt)}
          >
            <span>{prompt}</span>
            <ArrowRight size={16} className="prompt-arrow" />
          </button>
        ))}
      </div>
    </div>
  );
}
