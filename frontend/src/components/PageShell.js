import React from 'react';
import './page-shell.css';

export function PageShell({ title, actions, children }) {
  return (
    <>
      <a href="#main-content" className="skip-link">Skip to main content</a>
      <div className="page-shell" role="main" id="main-content" aria-labelledby="page-shell-title">
        <div className="page-header">
          <h1 id="page-shell-title" className="page-title" tabIndex={-1}>{title}</h1>
          {actions && <div className="page-actions">{actions}</div>}
        </div>
        <div className="page-content" role="region" aria-label={title + ' content'}>
          {children}
        </div>
      </div>
    </>
  );
}
export default PageShell;
