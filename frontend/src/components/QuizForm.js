import React, { useState, useEffect } from 'react';
import './quiz-form.css';
import client from '../api/client';

export function QuizForm(){
  const [questions,setQuestions] = useState([]);
  const [answers,setAnswers] = useState({});
  const [submitted,setSubmitted] = useState(null);
  const [error,setError] = useState(null);
  const [loading,setLoading] = useState(false);

  useEffect(()=>{ setLoading(true); client.get('/quiz').then(r=>{ setQuestions(r.data.questions);}).catch(e=>setError(e.message)).finally(()=>setLoading(false));},[]);

  const update = (id,value)=> setAnswers(a=>({...a,[id]: value}));
  const allAnswered = questions.length>0 && questions.every(q=> (answers[q.id]||'').trim().length>0);

  const submit = ()=>{
    if(!allAnswered) return;
    const answerStr = Object.entries(answers).map(([id,v])=> `${id}:${v}`).join('|');
  client.post(`/quiz/submit?answers=${encodeURIComponent(answerStr)}`)
      .then(r=> setSubmitted(r.data))
      .catch(e=> setError(e.message));
  };

  return (
    <div className="quiz-form" aria-label="Canonical quiz form">
      {loading && <p>Loading...</p>}
      {error && <p role="alert">Error: {error}</p>}
      {!loading && questions.map(q => (
        <div key={q.id} className="quiz-q">
          <label htmlFor={`q-${q.id}`}>{q.question_text}</label>
          <input id={`q-${q.id}`} value={answers[q.id]||''} onChange={e=>update(q.id,e.target.value)} aria-required="true" />
          {!submitted && (answers[q.id]||'').trim()==='' && <span className="q-hint" role="note">Required</span>}
        </div>
      ))}
      <div className="quiz-actions">
        <button className="btn" disabled={!allAnswered} onClick={submit} aria-label="Submit quiz">Submit</button>
      </div>
      {submitted && <div className="quiz-result" aria-live="polite">
        <p className="score">Score: {submitted.score}/{submitted.total}</p>
        {submitted.score === submitted.total && <p className="perfect" role="status">Perfect Score ✓</p>}
      </div>}
    </div>
  );
}
export default QuizForm;
