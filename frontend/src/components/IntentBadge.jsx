import React from 'react';
import { Tag } from 'lucide-react';
import { formatIntent } from '../utils/formatters';

export default function IntentBadge({ intent }) {
  if (!intent) return null;

  return (
    <span className="intent-badge" title={`Classified Intent: ${intent}`}>
      <Tag size={12} />
      <span>Intent: {formatIntent(intent)}</span>
    </span>
  );
}
