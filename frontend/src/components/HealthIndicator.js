import React, { useEffect, useState } from 'react';
import client from '../api/client';

export default function HealthIndicator(){
  const [status,setStatus] = useState('loading');
  const [version,setVersion] = useState('');
  useEffect(()=>{
    let active = true;
    const fetch = ()=> client.get('/health').then(r=>{ if(!active) return; setStatus('ok'); setVersion(r.data.version); }).catch(()=>{ if(!active) return; setStatus('error'); });
    fetch();
    const id = setInterval(fetch, 30000); // 30s poll
    return ()=> { active=false; clearInterval(id); };
  },[]);
  const color = status==='ok' ? 'var(--success,#0a4)' : (status==='error' ? 'var(--danger,#822)' : '#555');
  return <span aria-label={`API health ${status}`} style={{display:'inline-flex', alignItems:'center', gap:4, fontSize:'0.75rem', padding:'2px 6px', borderRadius:4, background:color, color:'#fff'}}>API {status==='ok'? '✓': status==='error'?'✕':'…'}{version && status==='ok' && ` v${version}`}</span>;
}
