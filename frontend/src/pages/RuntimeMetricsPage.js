import React, { useState } from 'react';
import axios from 'axios';
import RuntimeMetricsTable from '../components/RuntimeMetricsTable';

export default function RuntimeMetricsPage(){
  const [data,setData] = useState(null);
  const [error,setError] = useState(null);
  const [token,setToken] = useState('');
  const [unauthorized,setUnauthorized] = useState(false);
  const load = ()=>{
    setUnauthorized(false); setError(null); setData(null);
    const headers = token ? { 'X-Internal-Token': token } : {};
    axios.get('/internal/runtime-metrics', { headers })
      .then(r=>setData(r.data))
      .catch(e=>{
        if(e.response && e.response.status === 401) setUnauthorized(true); else setError(e.message);
      });
  };
  return <div style={{display:'flex', flexDirection:'column', gap:'1rem'}}>
    <div style={{display:'flex', gap:'0.75rem', alignItems:'flex-end', flexWrap:'wrap'}}>
      <div style={{display:'flex', flexDirection:'column', gap:'4px'}}>
        <label htmlFor="rt-token">Internal Token (optional)</label>
        <input id="rt-token" value={token} onChange={e=>setToken(e.target.value)} />
      </div>
      <button className="btn" onClick={load}>Load Snapshot</button>
    </div>
    <RuntimeMetricsTable data={data} error={error} unauthorized={unauthorized} />
  </div>;
}
