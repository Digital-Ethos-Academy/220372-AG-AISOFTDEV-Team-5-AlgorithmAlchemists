import React from 'react';
import './runtime-metrics-table.css';

export function RuntimeMetricsTable({ data, error, unauthorized }){
  if(error) return <p role="alert">Error: {error}</p>;
  if(unauthorized) return <div className="unauth" role="alert">Unauthorized – provide valid internal token.</div>;
  if(!data) return <p>Load runtime metrics to view snapshot.</p>;
  const endpoints = Object.entries(data.endpoints||{});
  return (
    <div className="runtime-table" aria-label="Runtime metrics table">
      <div className="summary-line">Uptime: {Math.round(data.uptime_seconds)}s · Endpoints: {endpoints.length}</div>
      <table>
        <thead><tr><th>Endpoint</th><th>Count</th><th>Avg (ms)</th><th>p95 (ms)</th></tr></thead>
        <tbody>
          {endpoints.map(([ep,val]) => (
            <tr key={ep}>
              <td>{ep}</td>
              <td>{val.count}</td>
              <td>{val.avg_ms}</td>
              <td className={val.p95_ms>500?'warn':''}>{val.p95_ms}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
export default RuntimeMetricsTable;
