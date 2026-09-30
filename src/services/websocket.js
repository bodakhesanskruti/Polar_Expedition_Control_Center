export function connectLive(onMessage,onStatus=()=>{}) {
  const base=import.meta.env.VITE_WS_URL || 'ws://127.0.0.1:8000/ws/live';
  const ws=new WebSocket(base);
  ws.onopen=()=>onStatus(true); ws.onclose=()=>onStatus(false); ws.onerror=()=>onStatus(false);
  ws.onmessage=e=>{try{onMessage(JSON.parse(e.data))}catch{onMessage(e.data)}};
  return ws;
}
