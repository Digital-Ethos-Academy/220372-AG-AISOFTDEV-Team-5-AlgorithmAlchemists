import React, { useState, useRef } from 'react';
import client from '../api/client';
import RecommendationList from '../components/RecommendationList';
import SkeletonBlock from '../components/SkeletonBlock';

function useAbortController(){
  const ref = useRef();
  if(!ref.current) ref.current = { ctrl: null };
  const next = () => {
    if(ref.current.ctrl) ref.current.ctrl.abort();
    ref.current.ctrl = new AbortController();
    return ref.current.ctrl.signal;
  };
  return next;
}

export default function RecommendationPage(){
  const [userId,setUserId] = useState('demo');
  const [data,setData] = useState(null);
  const [error,setError] = useState(null);
  const [loading,setLoading] = useState(false);
  const makeSignal = useAbortController();
  const run = ()=>{
    setError(null); setLoading(true); setData(null);
    client.post(`/recommendation?user_id=${encodeURIComponent(userId)}`, {}, { signal: makeSignal() })
      .then(r=>setData(r.data))
      .catch(e=>{ if(e.name !== 'CanceledError') setError(e.message); })
      .finally(()=> setLoading(false));
  };
  return <div aria-labelledby="rec-heading">
    <div style={{display:'flex', gap:'1rem', alignItems:'flex-end', flexWrap:'wrap'}}>
      <div style={{display:'flex', flexDirection:'column', gap:'4px'}}>
        <label htmlFor="user-id">User ID</label>
        <input id="user-id" value={userId} onChange={e=>setUserId(e.target.value)} aria-label="User ID input" />
      </div>
      <button className="btn" onClick={run} aria-label="Get recommendation button" disabled={loading}>{loading?'Loading…':'Recommend'}</button>
    </div>
    {error && <p role="alert" style={{marginTop:'1rem'}}>Error: {error}</p>}
    {loading && !data && <div style={{marginTop:'1rem', display:'flex', flexDirection:'column', gap:6}} aria-label="Loading recommendation">
      <SkeletonBlock width="220px" />
      <SkeletonBlock width="60%" />
      <SkeletonBlock width="80%" />
    </div>}
    {data && !loading && <div style={{marginTop:'1rem'}}><RecommendationList data={data} /></div>}
  </div>;
}
