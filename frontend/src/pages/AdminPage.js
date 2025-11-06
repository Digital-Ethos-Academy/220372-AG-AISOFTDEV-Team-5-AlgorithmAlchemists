import React, { useState } from 'react';
import client from '../api/client';

export default function AdminPage(){
  const [teams,setTeams] = useState([]);
  const [facts,setFacts] = useState([]);
  const [quiz,setQuiz] = useState([]);
  const [error,setError] = useState(null);
  const [token,setToken] = useState(()=> localStorage.getItem('adminToken') || '');

  const saveToken = () => {
    localStorage.setItem('adminToken', token);
  };

  const loadAll = async ()=>{
    setError(null);
    try {
      const [t,f,q] = await Promise.all([
        client.get('/admin/teams'),
        client.get('/admin/facts'),
        client.get('/admin/quiz/questions')
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
    {/* Minimal CRUD forms */}
    <div style={{marginTop:'1rem', display:'flex', flexWrap:'wrap', gap:'1rem'}}>
      <CreateTeamForm onDone={loadAll} />
      <CreateFactForm onDone={loadAll} />
      <CreateQuizQuestionForm onDone={loadAll} />
    </div>
    {error && <p role="alert" style={{color:'var(--danger,#c00)'}}>{error}</p>}
    <div style={{display:'grid', gap:'1rem', gridTemplateColumns:'repeat(auto-fit,minmax(250px,1fr))'}}>
      <section aria-label="Teams list">
        <h3>Teams ({teams.length})</h3>
        <ul>{teams.map(t=> <li key={t.id}>{t.id}: {t.name} <DeleteBtn endpoint={`/admin/teams/${t.id}`} onDone={loadAll} /></li>)}</ul>
      </section>
      <section aria-label="Facts list">
        <h3>Facts ({facts.length})</h3>
        <ul>{facts.map(f=> <li key={f.id}>{f.id}: {f.fact_text} <DeleteBtn endpoint={`/admin/facts/${f.id}`} onDone={loadAll} /></li>)}</ul>
      </section>
      <section aria-label="Quiz questions">
        <h3>Quiz Questions ({quiz.length})</h3>
        <ul>{quiz.map(q=> <li key={q.id}>{q.id}: {q.question_text} <DeleteBtn endpoint={`/admin/quiz/questions/${q.id}`} onDone={loadAll} /></li>)}</ul>
      </section>
    </div>
  </div>;
}

function DeleteBtn({ endpoint, onDone }){
  const [busy,setBusy] = useState(false);
  const del = ()=>{
    if(busy) return; setBusy(true);
    client.delete(endpoint).then(()=>onDone&&onDone()).catch(()=>{}).finally(()=>setBusy(false));
  };
  return <button aria-label="Delete" onClick={del} disabled={busy} style={{background:'#521', color:'#fff', border:'none', padding:'2px 6px', marginLeft:4, borderRadius:3}}>×</button>;
}

function CreateTeamForm({ onDone }){
  const [id,setId] = useState('');
  const [name,setName] = useState('');
  const submit = e => {
    e.preventDefault();
    if(!id || !name) return;
    client.post('/admin/teams', { id, name, mission:'Demo mission', responsibilities:['API','Docs'] })
      .then(()=>{ setId(''); setName(''); onDone&&onDone(); })
      .catch(()=>{});
  };
  return <form onSubmit={submit} style={{display:'flex', flexDirection:'column', gap:4, minWidth:220}} aria-label="Create team form">
    <strong>Create Team</strong>
    <input placeholder="Team ID" value={id} onChange={e=>setId(e.target.value)} />
    <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
    <button className="btn" disabled={!id||!name}>Add</button>
  </form>;
}

function CreateFactForm({ onDone }){
  const [id,setId] = useState('');
  const [text,setText] = useState('');
  const submit = e => { e.preventDefault(); if(!id||!text) return; client.post('/admin/facts', { id, category:'demo', fact_text:text }).then(()=>{ setId(''); setText(''); onDone&&onDone();}).catch(()=>{}); };
  return <form onSubmit={submit} style={{display:'flex', flexDirection:'column', gap:4, minWidth:220}} aria-label="Create fact form">
    <strong>Create Fact</strong>
    <input placeholder="Fact ID" value={id} onChange={e=>setId(e.target.value)} />
    <input placeholder="Text" value={text} onChange={e=>setText(e.target.value)} />
    <button className="btn" disabled={!id||!text}>Add</button>
  </form>;
}

function CreateQuizQuestionForm({ onDone }){
  const [id,setId] = useState('');
  const [q,setQ] = useState('');
  const submit = e => { e.preventDefault(); if(!id||!q) return; client.post('/admin/quiz/questions', { id, question_text:q, correct_answer:'answer', fact_id:'F1' }).then(()=>{ setId(''); setQ(''); onDone&&onDone();}).catch(()=>{}); };
  return <form onSubmit={submit} style={{display:'flex', flexDirection:'column', gap:4, minWidth:220}} aria-label="Create quiz question form">
    <strong>Create Quiz Q</strong>
    <input placeholder="Question ID" value={id} onChange={e=>setId(e.target.value)} />
    <input placeholder="Text" value={q} onChange={e=>setQ(e.target.value)} />
    <button className="btn" disabled={!id||!q}>Add</button>
  </form>;
}
