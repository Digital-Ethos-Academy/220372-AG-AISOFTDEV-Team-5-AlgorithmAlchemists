import React, { useState } from 'react';
import axios from 'axios';

export default function AdminPage(){
  const [teams,setTeams] = useState([]);
  const [facts,setFacts] = useState([]);
  const [quiz,setQuiz] = useState([]);
  const [error,setError] = useState(null);
  const [token,setToken] = useState(()=> localStorage.getItem('adminToken') || '');

  const saveToken = ()=>{
    localStorage.setItem('adminToken', token);
    axios.defaults.headers.common['X-Admin-Token'] = token;
  };

  const loadAll = async ()=>{
    setError(null);
    try {
      const [t,f,q] = await Promise.all([
        axios.get('/admin/teams'),
        axios.get('/admin/facts'),
        axios.get('/admin/quiz/questions')
      ]);
      setTeams(t.data);
      setFacts(f.data);
      setQuiz(q.data);
    } catch(e){
      setError(e.message);
    }
  };

  return <div style={{display:'flex', flexDirection:'column', gap:'1rem'}} aria-labelledby="admin-heading">
    <h2 id="admin-heading">Admin (Read-only)</h2>
    <p style={{fontSize:'0.85rem'}}>Provide admin API key (X-Admin-Token) to view seeded data. This page is read-only in the demo.</p>
    <div style={{display:'flex', gap:'0.5rem', flexWrap:'wrap'}}>
      <input aria-label="Admin token" placeholder="Admin token" value={token} onChange={e=>setToken(e.target.value)} style={{minWidth:'240px'}} />
      <button className="btn" onClick={saveToken}>Save Token</button>
      <button className="btn" onClick={loadAll}>Load Data</button>
    </div>
    {error && <p role="alert" style={{color:'var(--danger,#c00)'}}>{error}</p>}
    <div style={{display:'grid', gap:'1rem', gridTemplateColumns:'repeat(auto-fit,minmax(250px,1fr))'}}>
      <section aria-label="Teams list">
        <h3>Teams ({teams.length})</h3>
        <ul>{teams.map(t=> <li key={t.id}>{t.id}: {t.name}</li>)}</ul>
      </section>
      <section aria-label="Facts list">
        <h3>Facts ({facts.length})</h3>
        <ul>{facts.map(f=> <li key={f.id}>{f.id}: {f.fact_text}</li>)}</ul>
      </section>
      <section aria-label="Quiz questions">
        <h3>Quiz Questions ({quiz.length})</h3>
        <ul>{quiz.map(q=> <li key={q.id}>{q.id}: {q.question_text}</li>)}</ul>
      </section>
    </div>
  </div>;
}
