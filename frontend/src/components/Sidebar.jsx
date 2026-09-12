import React from 'react';
import { Plus, MessageSquare, Trash2, X, Database, Sparkles, ShieldCheck } from 'lucide-react';

export default function Sidebar({
  isOpen,
  onClose,
  conversations,
  activeId,
  onSelectConversation,
  onNewConversation,
  onDeleteConversation,
}) {
  return (
    <>
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <div className="brand-badge">
            <div className="brand-logo-icon">a</div>
            <span className="brand-title">Customer Care</span>
          </div>
          <button
            className="btn-sidebar-close"
            onClick={onClose}
            aria-label="Close sidebar"
            title="Close sidebar"
          >
            <X size={18} />
          </button>
        </div>

        <div className="new-chat-wrapper">
          <button
            className="btn-new-chat"
            onClick={onNewConversation}
            title="Start a new conversation"
          >
            <Plus size={18} />
            <span>New conversation</span>
          </button>
        </div>

        <div className="sidebar-section-title">Conversation History</div>

        <div className="history-list">
          {conversations.length === 0 ? (
            <div className="empty-history">
              <p>No previous conversations</p>
            </div>
          ) : (
            conversations.map((conv) => (
              <div
                key={conv.id}
                className={`history-item ${conv.id === activeId ? 'active' : ''}`}
                onClick={() => onSelectConversation(conv.id)}
              >
                <div className="history-info">
                  <MessageSquare size={15} style={{ flexShrink: 0, opacity: 0.7 }} />
                  <span className="history-title" title={conv.title || 'New inquiry'}>
                    {conv.title || 'Support Inquiry'}
                  </span>
                </div>
                <button
                  className="btn-delete-conv"
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteConversation(conv.id);
                  }}
                  title="Delete conversation"
                  aria-label="Delete conversation"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            ))
          )}
        </div>

        <div className="sidebar-footer">
          <div className="agent-info-card">
            <div className="agent-info-header">
              <Database size={15} color="#FF9900" />
              <span>About the Agent</span>
              <span className="rag-pill">RAG Powered</span>
            </div>
            <p className="agent-info-body">
              Enterprise customer service pipeline using intent classification, historical resolution vector search, and automated escalation safeguards.
            </p>
            <div className="agent-tech-specs">
              <span className="spec-tag">FAISS Index</span>
              <span className="spec-tag">all-MiniLM-L6-v2</span>
              <span className="spec-tag">Groq LLM</span>
            </div>
          </div>
        </div>
      </aside>

      <div
        className={`sidebar-backdrop ${isOpen ? 'open' : ''}`}
        onClick={onClose}
        aria-hidden="true"
      />
    </>
  );
}
