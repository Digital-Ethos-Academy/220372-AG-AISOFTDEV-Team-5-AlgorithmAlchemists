// Lightweight pub/sub for global error notifications.
// Keeps last N errors (bounded) for banner & debug panel.
const MAX_ERRORS = 50;
export const errorBus = {
  _errors: [],
  listeners: new Set(),
  push(err){
    if(!err || !err.message) return;
    this._errors.unshift({ ...err, ts: Date.now() });
    if(this._errors.length > MAX_ERRORS) this._errors.pop();
    this._emit();
  },
  clear(){ this._errors = []; this._emit(); },
  dismiss(ts){ this._errors = this._errors.filter(e => e.ts !== ts); this._emit(); },
  subscribe(cb){ this.listeners.add(cb); cb(this._errors); return () => { this.listeners.delete(cb); }; },
  _emit(){ for(const l of this.listeners) l(this._errors); }
};

export function useErrors(){
  const [errors,setErrors] = require('react').useState(()=> errorBus._errors);
  require('react').useEffect(()=> errorBus.subscribe(setErrors),[]);
  return errors;
}