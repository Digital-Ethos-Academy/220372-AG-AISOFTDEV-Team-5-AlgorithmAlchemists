// Bus for successful request traces (latency & trace_id).
const MAX = 100;
export const traceBus = {
  _items: [],
  listeners: new Set(),
  push(t){ if(!t) return; this._items.unshift({ ...t, ts: Date.now() }); if(this._items.length>MAX) this._items.pop(); this._emit(); },
  clear(){ this._items = []; this._emit(); },
  subscribe(cb){ this.listeners.add(cb); cb(this._items); return () => this.listeners.delete(cb); },
  _emit(){ for(const l of this.listeners) l(this._items); }
};
export function useTraces(){
  const React = require('react');
  const [items,setItems] = React.useState(()=> traceBus._items);
  React.useEffect(()=> traceBus.subscribe(setItems),[]);
  return items;
}