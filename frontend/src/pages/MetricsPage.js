import React, { useEffect, useState } from 'react';
import client from '../api/client';
import MetricsDashboard from '../components/MetricsDashboard';

export default function MetricsPage(){
  const [data,setData] = useState(null);
  const [error,setError] = useState(null);
  useEffect(()=>{ client.get('/metrics').then(r=>setData(r.data)).catch(e=>setError(e.message)); },[]);
  return <div>
    {error && <p role="alert">Error: {error}</p>}
    <MetricsDashboard data={data} />
  </div>;
}
