import React from 'react';
import { User, Bot, Clock } from 'lucide-react';
import IntentBadge from './IntentBadge';
import DecisionBadge from './DecisionBadge';
import ReasoningAccordion from './ReasoningAccordion';
import EvidencePanel from './EvidencePanel';
import { formatMessageTime } from '../utils/formatters';

export default function ChatMessage({ message }) {
  const isCustomer = message.role === 'customer';

  return (
    <div className={`message-row ${isCustomer ? 'customer' : 'assistant'}`}>
      <div className="message-card">
        <div className="message-header-info">
          <span className="author-label">
            {isCustomer ? (
              <>
                <User size={13} />
                <span>You</span>
              </>
            ) : (
              <>
                <Bot size={13} color="#ff9900" />
                <span>AI Support</span>
              </>
            )}
          </span>
          <span className="message-timestamp">
            {formatMessageTime(message.timestamp)}
          </span>
        </div>

        <div className="message-bubble">
          {/* Main message text */}
          <div className="response-text">
            {isCustomer ? message.text : message.response || message.text}
          </div>

          {/* AI metadata, badges, accordion reasoning, and RAG evidence */}
          {!isCustomer && (
            <>
              {/* Badges row: Intent and Decision */}
              {(message.intent || message.decision) && (
                <div className="metadata-bar">
                  {message.intent && <IntentBadge intent={message.intent} />}
                  {message.decision && <DecisionBadge decision={message.decision} />}
                </div>
              )}

              {/* Collapsible reasoning section */}
              {message.reason && (
                <ReasoningAccordion reason={message.reason} />
              )}

              {/* Collapsible RAG evidence section */}
              {Array.isArray(message.evidence) && message.evidence.length > 0 && (
                <EvidencePanel evidence={message.evidence} />
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
