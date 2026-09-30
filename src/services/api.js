const BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';
async function request(path, options={}) {
  const res = await fetch(`${BASE}${path}`, {headers:{'Content-Type':'application/json', ...(options.headers||{})}, ...options});
  if (!res.ok) { let msg=`Request failed (${res.status})`; try { const d=await res.json(); msg=d.detail||msg } catch{} throw new Error(msg) }
  return res.status===204 ? null : res.json();
}
export const api = {
  health:()=>request('/health'), stats:()=>request('/dashboard/stats'), expeditions:()=>request('/expeditions'),
  cargo:()=>request('/cargo'), tracking:()=>request('/cargo/tracking'), live:()=>request('/locations/live'),
  personnel:()=>request('/personnel'), inventory:()=>request('/inventory'), lowStock:()=>request('/inventory/low-stock'),
  alerts:()=>request('/alerts/open'), incidents:()=>request('/emergency/incidents'),
  resolveAlert:(id)=>request(`/alerts/${id}/resolve`,{method:'PATCH'}),
  updateCargo:(id,status)=>request(`/cargo/${id}/status`,{method:'PATCH',body:JSON.stringify({status})}),
  sos:(body)=>request('/emergency/sos',{method:'POST',body:JSON.stringify(body)}),
  addCheckin:(body)=>request('/checkins',{method:'POST',body:JSON.stringify(body)}),
};
export const API_BASE=BASE;
