import React from 'react';
import MetricsDashboard from '../components/MetricsDashboard';

export default { title: 'Components/MetricsDashboard', component: MetricsDashboard };

const healthy = {
  baseline_hours: 120,
  tool_hours: 48,
  compression_pct: 60,
  confidence_coverage: 78,
  quiz_accuracy: 90
};

const degraded = {
  baseline_hours: 120,
  tool_hours: 70,
  compression_pct: 42, // below target
  confidence_coverage: 45, // low coverage
  quiz_accuracy: 67 // warning state
};

export const Healthy = () => <div style={{padding:'2rem'}}><MetricsDashboard data={healthy} /></div>;
export const Degraded = () => <div style={{padding:'2rem'}}><MetricsDashboard data={degraded} /></div>;
