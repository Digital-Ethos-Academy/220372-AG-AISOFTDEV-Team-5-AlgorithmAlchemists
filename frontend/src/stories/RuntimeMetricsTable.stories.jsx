import React from 'react';
import RuntimeMetricsTable from '../components/RuntimeMetricsTable';

export default { title: 'Components/RuntimeMetricsTable', component: RuntimeMetricsTable };

const sample = {
  uptime_seconds: 732,
  endpoints: {
    '/overview': { count: 12, avg_ms: 18, p95_ms: 40 },
    '/recommendation': { count: 5, avg_ms: 120, p95_ms: 480 },
    '/qa': { count: 20, avg_ms: 90, p95_ms: 510 }
  }
};

export const Snapshot = () => <div style={{padding:'2rem'}}><RuntimeMetricsTable data={sample} /></div>;
export const Unauthorized = () => <div style={{padding:'2rem'}}><RuntimeMetricsTable unauthorized /></div>;
