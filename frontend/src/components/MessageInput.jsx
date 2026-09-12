import React, { useState, useRef, useEffect } from 'react';
import { Send, CornerDownLeft } from 'lucide-react';

export default function MessageInput({ onSendMessage, isLoading, disabled }) {
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  // Auto-resize textarea as user types
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 140)}px`;
    }
  }, [input]);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (isLoading || disabled) return;

    const trimmed = input.trim();
    if (!trimmed) return;

    onSendMessage(trimmed);
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    // Enter sends message, Shift+Enter creates newline
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="input-section">
      <form className="input-container" onSubmit={handleSubmit}>
        <div className="input-box-wrapper">
          <textarea
            ref={textareaRef}
            className="chat-textarea"
            placeholder="Type your message... (e.g. Where is my order?)"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={isLoading || disabled}
            aria-label="Message input"
          />

          <button
            type="submit"
            className="btn-send-message"
            disabled={!input.trim() || isLoading || disabled}
            aria-label="Send message"
            title="Send message (Enter)"
          >
            <span>Send</span>
            <Send size={14} />
          </button>
        </div>

        <div className="input-helper-row">
          <span>Press <strong>Enter</strong> to send, <strong>Shift + Enter</strong> for new line</span>
          <span>RAG Retrieval Active</span>
        </div>
      </form>
    </div>
  );
}
