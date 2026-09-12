import React from 'react';
import { Bot } from 'lucide-react';

export default function TypingIndicator() {
  return (
    <div className="message-row assistant">
      <div className="typing-indicator-row">
        <Bot size={16} color="#FF9900" />
        <span>AI Support is thinking...</span>
        <div className="dots-wrapper">
          <span className="dot-pulse"></span>
          <span className="dot-pulse"></span>
          <span className="dot-pulse"></span>
        </div>
      </div>
    </div>
  );
}
