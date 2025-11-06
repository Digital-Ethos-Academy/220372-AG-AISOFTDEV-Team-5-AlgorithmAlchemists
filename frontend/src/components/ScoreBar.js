import React from 'react';
import './score-bar.css';

export function ScoreBar({ label, value, max=100, showValue=true, tone }){
  const pct = Math.min(100, Math.round((value / max) * 100));
  let classTone = 'neutral';
  if(tone){ classTone = tone; }
  else if(pct >= 80) classTone = 'success';
  else if(pct >= 60) classTone = 'warn';
  else classTone = 'danger';
  return (
    <div className="score-bar" aria-label={label}>
      <div className="score-bar-header">
        <span className="score-bar-label">{label}</span>
        {showValue && <span className="score-bar-value" aria-live="polite">{pct}%</span>}
      </div>
      <div className="score-bar-track" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
        <div className={`score-bar-fill tone-${classTone}`} style={{ width: pct + '%' }} />
      </div>
    </div>
  );
}
export default ScoreBar;
