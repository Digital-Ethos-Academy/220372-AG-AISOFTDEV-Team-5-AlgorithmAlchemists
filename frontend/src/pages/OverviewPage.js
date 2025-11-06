import React, { useEffect, useState } from 'react';
import client from '../api/client';
import ProviderStatus from '../components/ProviderStatus';
import GapsPanel from '../components/GapsPanel';
import HealthIndicator from '../components/HealthIndicator';

export default function OverviewPage(){
  const [data,setData] = useState(null);
  const [error,setError] = useState(null);
  const [integrity,setIntegrity] = useState(null); // { teamsOk, quizOk, expected }
  useEffect(()=>{ 
    client.get('/overview').then(r=>setData(r.data)).catch(e=>setError(e.message));
    // Derive seed integrity by parallel calls (quiz length) without blocking main mission text.
    Promise.all([
      client.get('/quiz').catch(()=>null)
    ]).then(([quiz])=>{
      const teamsOk = (data?.team_count || 0) >= 10; // will update after overview load
      const quizOk = quiz ? (quiz.data?.questions?.length >= 15) : false;
      setIntegrity({ teamsOk, quizOk, expected: { teams:10, quiz:15 } });
    });
  },[]);

  useEffect(()=>{ if(data && integrity){ setIntegrity(i => i ? { ...i, teamsOk: data.team_count >= i.expected.teams } : i); } },[data]);

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
      {integrity && <SeedIntegrity status={integrity} />}
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

function SeedIntegrity({ status }){
  const { teamsOk, quizOk, expected } = status;
  const healthy = teamsOk && quizOk;
  return <div aria-label="Seed integrity status" style={{marginTop:'0.5rem', padding:'6px 8px', borderRadius:4, background: healthy ? 'var(--success,#0a4)' : 'var(--warning,#b87d00)', color:'#fff', fontSize:'0.75rem'}}>
    Seed Integrity: {healthy ? 'Healthy' : 'Needs Reseed'}
    {!healthy && <span style={{marginLeft:8}}>({teamsOk? 'teams ok' : `teams<${expected.teams}`} ; {quizOk? 'quiz ok' : `quiz<${expected.quiz}`})</span>}
  </div>;
}
