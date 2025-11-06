import axios from 'axios';
import { errorBus } from './errorBus';
import { traceBus } from './traceBus';

// Unified client with interceptors for trace propagation, structured error normalization & broadcast.
const client = axios.create({ baseURL: '/' });

client.interceptors.request.use(cfg => {
  const admin = localStorage.getItem('adminToken');
  if (admin) cfg.headers['X-Admin-Token'] = admin;
  const internal = localStorage.getItem('internalToken');
  if (internal) cfg.headers['X-Internal-Token'] = internal;
  // Stable per-request trace id (short) if not provided.
  cfg.headers['X-Trace-Id'] = cfg.headers['X-Trace-Id'] || Date.now().toString(36) + Math.random().toString(16).slice(2,6);
  // Capture start time for latency metrics.
  cfg.metadata = { start: (typeof performance !== 'undefined' ? performance.now() : Date.now()) };
  return cfg;
});

client.interceptors.response.use(r => {
  const end = (typeof performance !== 'undefined' ? performance.now() : Date.now());
  const start = r.config?.metadata?.start || end;
  traceBus.push({
    trace_id: r.config?.headers?.['X-Trace-Id'],
    method: r.config?.method?.toUpperCase(),
    url: r.config?.url,
    status: r.status,
    latency_ms: Math.round(end - start)
  });
  return r;
}, err => {
  if (err && err.response && typeof err.response.data === 'object') {
    const d = err.response.data;
    err.message = d.message || err.message;
    err.error_code = d.error_code || 'UNSPECIFIED';
    err.trace_id = d.trace_id || err.config?.headers?.['X-Trace-Id'];
    err.status = err.response.status;
  }
  // Broadcast to global error bus (non-blocking).
  errorBus.push({
    message: err.message,
    error_code: err.error_code,
    trace_id: err.trace_id,
    status: err.status,
    url: err.config?.url,
    method: err.config?.method?.toUpperCase()
  });
  return Promise.reject(err);
});

export default client;
