import React, { useEffect, useState } from 'react';
import client from '../api/client';

export default function ProviderStatus(){
  const [data,setData] = useState(null);
  const [error,setError] = useState(null);
  useEffect(()=>{ client.get('/config/health').then(r=>setData(r.data)).catch(e=>setError(e.message)); },[]);
  if (error) return <p role="alert">Provider status error: {error}</p>;
  if (!data) return <p>Loading provider status…</p>;
  const providers = data.providers || {};
  return (
    <div className="provider-status" aria-label="Provider availability">
      <h3 style={{marginTop:0}}>Providers</h3>
      <ul style={{listStyle:'none', padding:0, display:'flex', flexWrap:'wrap', gap:'0.5rem'}}>
        {Object.entries(providers).map(([name,enabled]) => (
          <li key={name} style={{padding:'4px 8px', borderRadius:4, background: enabled? 'var(--success,#0a4)': 'var(--danger,#822)', color:'#fff'}} aria-label={`${name} provider ${enabled?'enabled':'missing'}`}>{name}{enabled?'✓':'✕'}</li>
        ))}
      </ul>
    </div>
  );
}
