import React, { useState } from 'react';
import { useTraces, traceBus } from '../api/traceBus';
import './trace-panel.css';

export default function TracePanel(){
  const traces = useTraces();
  const [open,setOpen] = useState(false);
  if(!traces.length) return null;
  const latest = traces[0];
  return (
    <div className={`trace-panel ${open?'open':''}`} aria-label="Trace debug panel">
      <button className="trace-toggle" onClick={()=>setOpen(o=>!o)} aria-expanded={open} aria-controls="trace-list" aria-label="Toggle trace panel">{open?'Close':'Traces'} ▤</button>
      <div className="trace-summary" title="Latest trace id">{latest.trace_id} · {latest.latency_ms}ms</div>
      {open && <div id="trace-list" className="trace-list" role="region" aria-label="Recent request traces">
        <ul>
          {traces.slice(0,25).map(t => (
            <li key={t.ts}><code>{t.method}</code> {t.url} <span className="status">{t.status}</span> <span className="latency">{t.latency_ms}ms</span> <code>{t.trace_id}</code></li>
          ))}
        </ul>
        <div className="trace-actions">
          <button onClick={()=>traceBus.clear()} aria-label="Clear traces" className="trace-btn">Clear</button>
        </div>
      </div>}
    </div>
  );
}