import React from 'react';
import './gap-badge.css';

export function GapBadge({ count }){
  if(!count) return null;
  return <span className="gap-badge" aria-label={count + ' gaps detected'}>{count} Gap{count>1?'s':''}</span>;
}
export default GapBadge;
