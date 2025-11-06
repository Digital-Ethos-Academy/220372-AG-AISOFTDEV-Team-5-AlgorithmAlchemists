import React from 'react';
import MetricsCard from '../components/MetricsCard';

export default { title: 'Components/MetricsCard', component: MetricsCard };

export const Variants = () => (
  <div style={{display:'flex', gap:'1rem', padding:'2rem'}}>
    <MetricsCard title="Compression" value="64.3%" description="Target ≥60%" tone="success" />
    <MetricsCard title="Coverage" value="78%" description="Below target" tone="warning" />
    <MetricsCard title="Latency p95" value="540ms" description="Needs optimization" tone="danger" />
  </div>
);
