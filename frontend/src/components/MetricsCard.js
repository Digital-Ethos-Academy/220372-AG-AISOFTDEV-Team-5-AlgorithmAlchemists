import React from 'react';
import './metrics-card.css';

export function MetricsCard({ title, value, description, tone='info'}){
  return (
    <div className={`metrics-card tone-${tone}`} role="group" aria-label={title}>
      <div className="metrics-title">{title}</div>
      <div className="metrics-value" aria-live="polite">{value}</div>
      {description && <div className="metrics-desc">{description}</div>}
    </div>
  );
}
export default MetricsCard;
