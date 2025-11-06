import React, { useState } from 'react';
import client from '../api/client';
import RecommendationList from '../components/RecommendationList';

export default function RecommendationPage(){
  const [userId,setUserId] = useState('demo');
  const [data,setData] = useState(null);
  const [error,setError] = useState(null);
  const run = ()=>{ client.post(`/recommendation?user_id=${encodeURIComponent(userId)}`).then(r=>setData(r.data)).catch(e=>setError(e.message)); };
  return <div aria-labelledby="rec-heading">
    <div style={{display:'flex', gap:'1rem', alignItems:'flex-end', flexWrap:'wrap'}}>
      <div style={{display:'flex', flexDirection:'column', gap:'4px'}}>
        <label htmlFor="user-id">User ID</label>
        <input id="user-id" value={userId} onChange={e=>setUserId(e.target.value)} aria-label="User ID input" />
      </div>
      <button className="btn" onClick={run} aria-label="Get recommendation button">Recommend</button>
    </div>
    {error && <p role="alert" style={{marginTop:'1rem'}}>Error: {error}</p>}
    {data && <div style={{marginTop:'1rem'}}><RecommendationList data={data} /></div>}
  </div>;
}
