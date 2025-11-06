import React, { useEffect, useState } from 'react';
import client from '../api/client';

export default function GapsPanel(){
  const [data,setData] = useState(null);
  const [error,setError] = useState(null);
  const [attempts,setAttempts] = useState(0);
  useEffect(()=>{ 
    let cancelled = false;
    const fetch = () => client.get('/gaps')
      .then(r=>{ if(cancelled) return; setData(r.data); })
      .catch(e=>{ if(cancelled) return; setError(e.message); if(attempts < 1){ setAttempts(a=>a+1); setTimeout(fetch, 800); } });
    fetch();
    return ()=> { cancelled = true; };
  },[attempts]);
  if(error) return <p role="alert">Gaps error: {error}</p>;
  if(!data) return <p>Loading gaps…</p>;
  return (
    <div className="gaps-panel" aria-label="Gaps summary">
      <h3 style={{marginTop:0}}>Gaps</h3>
      <p><strong>Total Teams:</strong> {data.summary.total_teams} · <strong>Gap Count:</strong> {data.summary.gap_count}</p>
      <ul style={{listStyle:'none', padding:0}}>
        {data.gaps.map((g,i)=> <li key={i} style={{marginBottom:4, padding:'4px 6px', background:'#332', borderRadius:4}}>{g.team_id}: {g.type} – {g.detail}</li>)}
      </ul>
    </div>
  );
}
