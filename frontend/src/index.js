import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import axios from 'axios';

// Initialize axios global headers from persisted values
function applyTenantHeader(){
  const tenant = localStorage.getItem('tenantId') || 'default';
  axios.defaults.headers.common['X-Tenant-Id'] = tenant;
}
applyTenantHeader();
const adminToken = localStorage.getItem('adminToken');
if (adminToken) axios.defaults.headers.common['X-Admin-Token'] = adminToken;
window.addEventListener('tenant-changed', ()=> applyTenantHeader());
import './theme.css';
import './design/tokens.css';

const container = document.getElementById('root');
const root = createRoot(container);
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
