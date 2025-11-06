import React from 'react';
import MetricsCard from './MetricsCard';
import ScoreBar from './ScoreBar';
import './metrics-dashboard.css';

export function MetricsDashboard({ data }) {
  if(!data) return null;
  const compression = Math.round(data.compression_pct);
  const coverage = Math.round(data.confidence_coverage||0);
  const quizAcc = Math.round(data.quiz_accuracy||0);
  return (
    <div className="metrics-dash" aria-label="Metrics dashboard">
      <div className="metrics-grid">
        <MetricsCard title="Baseline Hours" value={data.baseline_hours} description="Simulated" />
        <MetricsCard title="Tool Hours" value={data.tool_hours} description="Simulated" />
        <MetricsCard title="Compression" value={compression + '%'} description="Target ≥60%" tone={compression>=60?'success':'danger'} />
        <MetricsCard title="Quiz Accuracy" value={quizAcc + '%'} tone={quizAcc===100?'success':'warning'} />
      </div>
      <div className="metrics-bars">
        <ScoreBar label="Confidence Coverage" value={coverage} />
      </div>
    </div>
  );
}
export default MetricsDashboard;
