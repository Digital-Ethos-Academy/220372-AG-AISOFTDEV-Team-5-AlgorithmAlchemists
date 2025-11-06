import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function OverviewPage(){
  const [data,setData] = useState(null);
  const [error,setError] = useState(null);
  useEffect(()=>{
    axios.get('/overview').then(r=>setData(r.data)).catch(e=>setError(e.message));
  },[]);
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
    </>}
  </div>;
}
