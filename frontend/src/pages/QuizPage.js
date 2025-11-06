import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function QuizPage(){
  const [questions,setQuestions] = useState([]);
  const [answerIds,setAnswerIds] = useState({});
  const [result,setResult] = useState(null);
  const [error,setError] = useState(null);
  useEffect(()=>{ axios.get('/quiz').then(r=>setQuestions(r.data.questions)).catch(e=>setError(e.message)); },[]);
  const submit = ()=>{
    const answers = Object.keys(answerIds).filter(id=>answerIds[id]).join(',');
    axios.post(`/quiz/submit?answers=${encodeURIComponent(answers)}`).then(r=>setResult(r.data)).catch(e=>setError(e.message));
  };
  return <div className="card" aria-labelledby="quiz-heading">
    <h1 id="quiz-heading">Canonical Quiz</h1>
    {error && <p role="alert">Error: {error}</p>}
    <ul aria-label="Quiz question list">
      {questions.map(q=> <li key={q.id}>
        <label>
          <input type="checkbox" onChange={e=> setAnswerIds(a=>({...a,[q.id]: e.target.checked})) } aria-label={`Select answer ${q.id}`} /> {q.question_text}
        </label>
      </li>)}
    </ul>
    <button className="btn" onClick={submit} aria-label="Submit quiz button">Submit</button>
    {result && <div aria-live="polite" aria-label="Quiz results">
      <p>Score: {result.score}/{result.total}</p>
      <p>Correct IDs: {result.correct.join(', ')}</p>
    </div>}
  </div>;
}
