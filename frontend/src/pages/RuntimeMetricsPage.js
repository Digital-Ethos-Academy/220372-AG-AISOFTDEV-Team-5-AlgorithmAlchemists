import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function RuntimeMetricsPage(){
  const [data,setData] = useState(null);
  const [error,setError] = useState(null);
  const [token,setToken] = useState('');
  useEffect(()=>{ /* lazy load when token present */ },[]);
  const load = ()=>{
    const headers = token ? { 'X-Internal-Token': token } : {};
    axios.get('/internal/runtime-metrics', { headers }).then(r=>setData(r.data)).catch(e=>setError(e.message));
  };
  return <div className="card" aria-labelledby="runtime-heading">
    <h1 id="runtime-heading">Runtime Metrics (Internal)</h1>
    <label htmlFor="rt-token">Internal Token</label><br/>
    <input id="rt-token" value={token} onChange={e=>setToken(e.target.value)} aria-label="Internal token input" />
    <button className="btn" onClick={load} aria-label="Load runtime metrics button">Load</button>
    {error && <p role="alert">Error: {error}</p>}
    {data && <>
      <p>Uptime Seconds: {data.uptime_seconds}</p>
      <table aria-label="Runtime endpoints table"><thead><tr><th>Endpoint</th><th>Count</th><th>Avg ms</th><th>p95 ms</th></tr></thead><tbody>
        {Object.entries(data.endpoints).map(([ep,val])=> <tr key={ep}><td>{ep}</td><td>{val.count}</td><td>{val.avg_ms}</td><td>{val.p95_ms}</td></tr>)}
      </tbody></table>
    </>}
  </div>;
}
