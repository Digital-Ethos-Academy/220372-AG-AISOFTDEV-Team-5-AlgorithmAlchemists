import React, { useEffect, useState } from 'react';
import client from '../api/client';
import ProviderStatus from '../components/ProviderStatus';
import GapsPanel from '../components/GapsPanel';
import HealthIndicator from '../components/HealthIndicator';

export default function OverviewPage(){
  const [data,setData] = useState(null);
  const [error,setError] = useState(null);
  useEffect(()=>{ client.get('/overview').then(r=>setData(r.data)).catch(e=>setError(e.message)); },[]);
  return <div className="card" aria-labelledby="overview-heading">
    <h1 id="overview-heading">Project Overview</h1>
    {error && <p role="alert">Error: {error}</p>}
    {!data && !error && <p>Loading...</p>}
    {data && <>
      <p><strong>Mission:</strong> {data.mission}</p>
      <p><strong>Problem:</strong> {data.problem}</p>
      <p><strong>Value:</strong> {data.value}</p>
      <p><strong>Teams:</strong> {data.team_count}</p>
      <p><strong>Rationale:</strong> {data.rationale}</p>
      <div style={{display:'flex', flexWrap:'wrap', gap:'1rem', marginTop:'1rem'}}>
        <HealthIndicator />
        <ProviderStatus />
      </div>
      <div style={{marginTop:'1rem'}}>
        <GapsPanel />
      </div>
    </>}
  </div>;
}
