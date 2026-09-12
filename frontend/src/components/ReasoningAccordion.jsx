import React, { useState } from 'react';
import { HelpCircle, ChevronDown, ChevronUp } from 'lucide-react';

export default function ReasoningAccordion({ reason }) {
  const [isOpen, setIsOpen] = useState(false);

  if (!reason) return null;

  return (
    <div className="reasoning-card">
      <button
        type="button"
        className="reasoning-header"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
      >
        <div className="reasoning-label">
          <HelpCircle size={13} />
          <span>Why? Decision reasoning</span>
        </div>
        {isOpen ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
      </button>

      {isOpen && (
        <div className="reasoning-content">
          <p>{reason}</p>
        </div>
      )}
    </div>
  );
}
