import React, { useState } from 'react';
import { Database, ChevronDown, ChevronUp, MessageCircle, UserCheck } from 'lucide-react';

export default function EvidencePanel({ evidence = [] }) {
  const [isOpen, setIsOpen] = useState(false);

  if (!evidence || evidence.length === 0) return null;

  return (
    <div className="evidence-panel">
      <button
        type="button"
        className={`evidence-header-btn ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
      >
        <div className="evidence-title-group">
          <Database size={14} color="#ff9900" />
          <span>RAG Evidence</span>
          <span className="evidence-count-pill">{evidence.length}</span>
        </div>
        {isOpen ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
      </button>

      {isOpen && (
        <div className="evidence-items-container">
          {evidence.map((item, index) => (
            <div key={index} className="evidence-card">
              <div className="evidence-card-header">
                <span>Case Reference</span>
                <span className="conversation-id-tag">
                  Conversation #{item.conversation_id || index + 1}
                </span>
              </div>

              <div className="evidence-section">
                <div className="evidence-section-label">Customer Query</div>
                <div className="evidence-section-text">
                  {item.customer_query || 'No query text available'}
                </div>
              </div>

              <div className="evidence-section">
                <div className="evidence-section-label">Agent Reply</div>
                <div className="evidence-section-text">
                  {item.agent_reply || 'No agent reply recorded'}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
