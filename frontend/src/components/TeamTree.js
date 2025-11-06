import React, { useState } from 'react';
import './team-tree.css';

function TreeNode({ node }) {
  const [open,setOpen] = useState(true);
  const hasChildren = node.children && node.children.length > 0;
  return (
    <li className="team-node">
      <div className="team-node-line">
        {hasChildren && <button className="disclosure" aria-label={open? 'Collapse': 'Expand'} aria-expanded={open} onClick={()=>setOpen(o=>!o)}>{open? '−':'+'}</button>}
        <span className="team-name">{node.name}</span>
        {node.mission && <span className="team-mission" title={node.mission}>{node.mission}</span>}
      </div>
      {open && hasChildren && (
        <ul role="group">
          {node.children.map(c => <TreeNode key={c.id} node={c} />)}
        </ul>
      )}
    </li>
  );}

export function TeamTree({ data }) {
  return (
    <ul className="team-tree" role="tree" aria-label="Organization tree">
      {data.map(n => <TreeNode key={n.id} node={n} />)}
    </ul>
  );
}
export default TeamTree;
