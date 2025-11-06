import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Footer(){
  const [meta,setMeta] = useState(null);
  useEffect(()=>{
    let cancelled = false;
    axios.get('/health').then(r=>{ if(!cancelled) setMeta(r.data); }).catch(()=>{});
    return ()=>{ cancelled = true; };
  },[]);
  return (
    <footer style={{marginTop:'2rem', padding:'1rem', fontSize:'0.75rem', opacity:0.8}} aria-label="Build metadata footer">
      <span>POI Compass</span>
      {meta && <>
        <span style={{marginLeft:'1rem'}}>v{meta.version}</span>
        <span style={{marginLeft:'1rem'}}>commit: {meta.git_commit}</span>
        {meta.build_time && <span style={{marginLeft:'1rem'}}>built: {meta.build_time}</span>}
      </>}
    </footer>
  );
}
