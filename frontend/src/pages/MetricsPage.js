import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function MetricsPage(){
  const [data,setData] = useState(null);
  const [error,setError] = useState(null);
  useEffect(()=>{ axios.get('/metrics').then(r=>setData(r.data)).catch(e=>setError(e.message)); },[]);
  return <div className="card" aria-labelledby="metrics-heading">
    <h1 id="metrics-heading">Orientation Metrics</h1>
    {error && <p role="alert">Error: {error}</p>}
    {data && <table aria-label="Metrics table">
      <tbody>
        <tr><th>Baseline Hours</th><td>{data.baseline_hours}</td></tr>
        <tr><th>Tool Hours</th><td>{data.tool_hours}</td></tr>
        <tr><th>Compression %</th><td>{data.compression_pct}</td></tr>
        <tr><th>Quiz Accuracy</th><td>{data.quiz_accuracy}</td></tr>
        <tr><th>Confidence Coverage</th><td>{data.confidence_coverage}</td></tr>
      </tbody>
    </table>}
  </div>;
}
