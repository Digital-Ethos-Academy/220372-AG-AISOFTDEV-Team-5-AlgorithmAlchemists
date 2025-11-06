import React, { useState } from 'react';
import { useErrors, errorBus } from '../api/errorBus';
import './error-banner.css';

export default function ErrorBanner(){
  const errors = useErrors();
  const [expanded,setExpanded] = useState(false);
  if(!errors.length) return null;
  const latest = errors[0];
  return (
    <div className="error-banner" role="alert" aria-live="assertive">
      <div className="error-banner-row">
        <strong>Error:</strong> {latest.message}
        {latest.status && <span className="err-meta">({latest.status})</span>}
        <button aria-label="Toggle error details" onClick={()=>setExpanded(e=>!e)} className="err-btn">{expanded?'Hide':'Details'}</button>
        <button aria-label="Dismiss error" onClick={()=>errorBus.dismiss(latest.ts)} className="err-btn">×</button>
        <button aria-label="Clear all errors" onClick={()=>errorBus.clear()} className="err-btn" title="Clear all">Clear</button>
      </div>
      {expanded && (
        <div className="error-details" aria-label="Error details">
          <ul>
            {errors.slice(0,5).map(e => (
              <li key={e.ts}>
                <code>{e.error_code}</code> &middot; <code>{e.trace_id}</code> &middot; {e.method} {e.url}
              </li>
            ))}
          </ul>
          {errors.length > 5 && <p className="more" aria-label="More errors truncated">(+{errors.length - 5} more)</p>}
        </div>
      )}
    </div>
  );
}