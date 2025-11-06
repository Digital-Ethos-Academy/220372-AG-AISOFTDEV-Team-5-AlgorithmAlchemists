import React, { useState } from 'react';
import './roles-search-panel.css';
import axios from 'axios';

export function RolesSearchPanel(){
  const [query,setQuery] = useState('');
  const [results,setResults] = useState([]);
  const [loading,setLoading] = useState(false);
  const [error,setError] = useState(null);
  const [touched,setTouched] = useState(false);

  const search = async (e)=>{
    e && e.preventDefault();
    setTouched(true);
    if(!query.trim()) { setResults([]); return; }
    setLoading(true); setError(null);
    try {
      const r = await axios.get(`/roles?query=${encodeURIComponent(query)}`);
      setResults(r.data.matches || []);
    } catch(err){
      setError(err.message);
    } finally { setLoading(false); }
  };

  return (
    <div className="roles-search" aria-label="Role responsibility lookup">
      <form onSubmit={search} className="roles-form" aria-label="Roles search form">
        <div className="field-group">
          <label htmlFor="role-q">Search responsibilities</label>
          <input id="role-q" value={query} onChange={e=>setQuery(e.target.value)} placeholder="e.g. identity provisioning" />
        </div>
        <button className="btn" type="submit" disabled={loading}>Search</button>
      </form>
      {loading && <p>Searching…</p>}
      {error && <p role="alert">Error: {error}</p>}
      {!loading && touched && query.trim() && results.length===0 && <p role="status">No matches for "{query}"</p>}
      <ul className="roles-results" aria-label="Role results list">
        {results.map(r => (
          <li key={r.team_id} className="role-item">
            <div className="role-line">
              <span className="role-team">{r.team_name}</span>
              <span className="role-score" aria-label="match score">{r.score}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
export default RolesSearchPanel;
