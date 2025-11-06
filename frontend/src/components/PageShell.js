import React from 'react';
import './page-shell.css';

export function PageShell({ title, actions, children }) {
  return (
    <div className="page-shell">
      <div className="page-header">
        <h1 className="page-title" tabIndex={-1}>{title}</h1>
        {actions && <div className="page-actions">{actions}</div>}
      </div>
      <div className="page-content" role="region" aria-label={title + ' content'}>
        {children}
      </div>
    </div>
  );
}
export default PageShell;
