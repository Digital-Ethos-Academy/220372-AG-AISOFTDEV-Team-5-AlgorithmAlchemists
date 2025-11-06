import React, { useState, useRef } from 'react';
import client from '../api/client';
import QAResultPanel from '../components/QAResultPanel';
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

export default function QAPage(){
  const [question,setQuestion] = useState('');
  const [state,setState] = useState(null);
  const [error,setError] = useState(null);
  const [loading,setLoading] = useState(false);
  const makeSignal = useAbortController();
  const ask = async (e)=>{
    e.preventDefault();
    setError(null);
    try {
      setLoading(true); setState(null);
      const qa = await client.post('/qa', { question }, { signal: makeSignal() });
      let fallback = null;
      if(qa.data.confidence !== undefined && qa.data.confidence < 0.85){
        const fb = await client.post('/qa/fallback', { question }, { signal: makeSignal() });
        fallback = fb.data;
      }
      setState({ question, answer: qa.data.answer, confidence: qa.data.confidence, fallback });
    } catch (err){
      setError(err.message);
    } finally { setLoading(false); }
  };
  return (
    <div style={{display:'flex', flexDirection:'column', gap:'1rem'}}>
      <form onSubmit={ask} style={{display:'flex', gap:'0.5rem', alignItems:'flex-end', flexWrap:'wrap'}} aria-label="Q&A form" role="form">
        <div style={{display:'flex', flexDirection:'column', gap:'4px'}}>
          <label htmlFor="qa-q">Ask a project question</label>
          <input id="qa-q" value={question} onChange={e=>setQuestion(e.target.value)} placeholder="e.g. Who owns SSO integration?" required />
        </div>
        <button className="btn" type="submit" disabled={!question.trim()}>Ask</button>
      </form>
      {error && <p role="alert">Error: {error}</p>}
      {loading && !state && !error && <div style={{display:'flex', flexDirection:'column', gap:6}} aria-label="Loading answer">
        <SkeletonBlock width="240px" />
        <SkeletonBlock width="70%" />
        <SkeletonBlock width="50%" />
      </div>}
      <QAResultPanel state={state} />
    </div>
  );
}
