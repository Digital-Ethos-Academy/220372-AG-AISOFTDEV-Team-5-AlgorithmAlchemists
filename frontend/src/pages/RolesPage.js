import React, { useState } from 'react';
import axios from 'axios';

export default function RolesPage(){
  const [query,setQuery] = useState('');
  const [results,setResults] = useState([]);
  const [error,setError] = useState(null);
  const onSearch = (e)=>{ e.preventDefault(); axios.get(`/roles?query=${encodeURIComponent(query)}`).then(r=>setResults(r.data.matches)).catch(err=>setError(err.message)); };
  return <div className="card" aria-labelledby="roles-heading">
    <h1 id="roles-heading">Role Lookup</h1>
    <form onSubmit={onSearch} aria-label="Role search form">
      <label htmlFor="role-query">Query</label><br/>
      <input id="role-query" value={query} onChange={e=>setQuery(e.target.value)} aria-required="true" aria-label="Role search input" />
      <button className="btn" type="submit" aria-label="Search roles button">Search</button>
    </form>
    {error && <p role="alert">Error: {error}</p>}
    <ul aria-label="Role matches list">
      {results.map(m=> <li key={m.team_id}>{m.team_name} – score {m.score}</li>)}
    </ul>
  </div>;
}
