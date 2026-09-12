import React from 'react';
import { CheckCircle2, AlertTriangle } from 'lucide-react';
import { formatDecision } from '../utils/formatters';

export default function DecisionBadge({ decision }) {
  if (!decision) return null;

  const { isEscalation, title, badgeClass } = formatDecision(decision);

  return (
    <span className={`decision-badge ${badgeClass}`}>
      {isEscalation ? (
        <AlertTriangle size={13} strokeWidth={2.5} />
      ) : (
        <CheckCircle2 size={13} strokeWidth={2.5} />
      )}
      <span>{title}</span>
    </span>
  );
}
