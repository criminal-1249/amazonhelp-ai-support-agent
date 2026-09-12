import React, { useEffect, useRef } from 'react';
import { AlertCircle } from 'lucide-react';
import WelcomeScreen from './WelcomeScreen';
import ChatMessage from './ChatMessage';
import TypingIndicator from './TypingIndicator';

export default function ChatWindow({
  messages,
  isLoading,
  error,
  onSelectPrompt,
}) {
  const scrollEndRef = useRef(null);

  // Auto-scroll to the newest message or typing indicator
  useEffect(() => {
    if (scrollEndRef.current) {
      scrollEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isLoading]);

  return (
    <div className="chat-window">
      <div className="chat-content-container">
        {messages.length === 0 ? (
          <WelcomeScreen onSelectPrompt={onSelectPrompt} />
        ) : (
          messages.map((msg) => <ChatMessage key={msg.id} message={msg} />)
        )}

        {isLoading && <TypingIndicator />}

        {error && (
          <div className="error-banner" role="alert">
            <AlertCircle size={18} style={{ flexShrink: 0 }} />
            <span>{error}</span>
          </div>
        )}

        <div ref={scrollEndRef} style={{ height: 1 }} />
      </div>
    </div>
  );
}
