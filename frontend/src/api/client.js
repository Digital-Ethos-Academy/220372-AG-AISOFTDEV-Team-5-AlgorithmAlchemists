import axios from 'axios';

// Minimal unified client with interceptors for error normalization & token headers.
const client = axios.create({ baseURL: '/' });

client.interceptors.request.use(cfg => {
  // Inject admin & internal tokens if stored.
  const admin = localStorage.getItem('adminToken');
  if (admin) cfg.headers['X-Admin-Token'] = admin;
  const internal = localStorage.getItem('internalToken');
  if (internal) cfg.headers['X-Internal-Token'] = internal;
  cfg.headers['X-Trace-Id'] = cfg.headers['X-Trace-Id'] || Date.now().toString(36);
  return cfg;
});

client.interceptors.response.use(r => r, err => {
  if (err.response && typeof err.response.data === 'object') {
    const d = err.response.data;
    err.message = d.message || err.message;
    err.error_code = d.error_code;
    err.trace_id = d.trace_id;
  }
  return Promise.reject(err);
});

export default client;
