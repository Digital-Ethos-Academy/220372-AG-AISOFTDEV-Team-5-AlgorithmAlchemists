import React, { useState } from 'react';
import axios from 'axios';
import QAResultPanel from '../components/QAResultPanel';

export default function QAPage(){
  const [question,setQuestion] = useState('');
  const [state,setState] = useState(null);
  const [error,setError] = useState(null);
  const ask = async (e)=>{
    e.preventDefault();
    setError(null);
    try {
      const qa = await axios.post('/qa', { question });
      let fallback = null;
      if(qa.data.confidence !== undefined && qa.data.confidence < 0.85){
        const fb = await axios.post('/qa/fallback', { question });
        fallback = fb.data;
      }
      setState({ question, answer: qa.data.answer, confidence: qa.data.confidence, fallback });
    } catch (err){
      setError(err.message);
    }
  };
  return (
    <div style={{display:'flex', flexDirection:'column', gap:'1rem'}}>
      <form onSubmit={ask} style={{display:'flex', gap:'0.5rem', alignItems:'flex-end', flexWrap:'wrap'}} aria-label="Q&A form">
        <div style={{display:'flex', flexDirection:'column', gap:'4px'}}>
          <label htmlFor="qa-q">Ask a project question</label>
          <input id="qa-q" value={question} onChange={e=>setQuestion(e.target.value)} placeholder="e.g. Who owns SSO integration?" required />
        </div>
        <button className="btn" type="submit" disabled={!question.trim()}>Ask</button>
      </form>
      {error && <p role="alert">Error: {error}</p>}
      <QAResultPanel state={state} />
    </div>
  );
}
