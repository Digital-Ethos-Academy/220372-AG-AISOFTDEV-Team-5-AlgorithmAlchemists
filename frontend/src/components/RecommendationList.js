import React from 'react';
import './recommendation-list.css';

export function RecommendationList({ data }) {
  if(!data) return null;
  return (
    <div className="rec-list" aria-label="Recommendation details">
      <div className="rec-header"><span>Factor</span><span>Weight</span><span>Description</span></div>
      {data.explanation_breakdown && data.explanation_breakdown.map(b => (
        <div key={b.factor} className="rec-row">
          <span className="factor">{b.factor}</span>
          <span className="weight">{b.weight}</span>
          <span className="desc">{b.description}</span>
        </div>
      ))}
      <div className="rec-summary">Team {data.selected_team_id} · Confidence {Math.round(data.confidence*100)}%</div>
      <div className="rec-rationale" aria-label="Rationale">{data.rationale}</div>
    </div>
  );
}
export default RecommendationList;
