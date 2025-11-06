import React from 'react';
import './qa-result-panel.css';

export function QAResultPanel({ state }) {
  if(!state) return null;
  const { question, answer, confidence, fallback } = state;
  const low = confidence !== undefined && confidence < 0.85;
  return (
    <div className="qa-panel" aria-label="Q&A result">
      <div className="qa-header">
        <h2>Answer</h2>
        {confidence !== undefined && (
          <span className={`confidence-badge ${low?'low':'high'}`}>{Math.round(confidence*100)}%</span>
        )}
      </div>
      {low && fallback && <div className="fallback-banner" role="alert">Low confidence &lt; 0.85 – {fallback.escalation_action || 'Consult Mentor'}</div>}
      <p className="qa-q"><strong>Q:</strong> {question}</p>
      <p className="qa-a"><strong>A:</strong> {answer}</p>
    </div>
  );
}
export default QAResultPanel;
