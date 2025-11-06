import React, { useEffect, useState } from 'react';
import client from '../api/client';
import TeamTree from '../components/TeamTree';

export default function OrgPage(){
  const [teams,setTeams] = useState([]);
  const [error,setError] = useState(null);
  useEffect(()=>{ client.get('/org').then(r=>setTeams(r.data.teams)).catch(e=>setError(e.message)); },[]);
  // Simple flatten to tree (mock data may already be hierarchical; if not we group by parent_team_id)
  const byParent = {}; teams.forEach(t => { const p = t.parent_team_id || 'root'; (byParent[p] = byParent[p] || []).push(t); });
  function build(id){
    return (byParent[id]||[]).map(node => ({
      id: node.id,
      name: node.name,
      mission: node.mission,
      children: build(node.id)
    }));
  }
  const tree = build('root');
  return <div aria-labelledby="org-heading">
    {error && <p role="alert">Error: {error}</p>}
    <TeamTree data={tree} />
  </div>;
}
