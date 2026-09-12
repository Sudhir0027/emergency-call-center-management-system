import { useEffect,useState } from "react";
import { Link } from "react-router-dom";
import api,{messageOf} from "../services/api";
import PriorityBadge from "../components/PriorityBadge";
import StatusBadge from "../components/StatusBadge";
export default function Queue(){
 const[queue,setQueue]=useState([]),[error,setError]=useState("");
 const load=()=>api.get("/calls/queue").then(r=>setQueue(r.data)).catch(e=>setError(messageOf(e)));
 useEffect(()=>{load();const t=setInterval(load,5000);return()=>clearInterval(t)},[]);
 const next=async()=>{try{const r=await api.get("/calls/next");window.location.href=`/calls/${r.data.call_id}`}catch(e){setError(messageOf(e))}};
 return <div className="space-y-5"><div className="flex flex-col sm:flex-row justify-between gap-3"><div><h2 className="text-2xl font-bold">Emergency Priority Queue</h2><p className="text-sm text-slate-500">ORDER: priority DESC → Call ID ASC</p></div><button onClick={next} className="bg-red-600 text-white px-4 py-2.5 rounded-xl font-semibold">Process Next Emergency</button></div>{error&&<p className="text-red-600">{error}</p>}
 <div className="card p-2 overflow-x-auto"><table className="w-full text-sm"><thead><tr className="text-left text-xs uppercase text-slate-500 border-b"><th className="p-3">Position</th><th>Call ID</th><th>Type</th><th>Location</th><th>Priority</th><th>Status</th><th></th></tr></thead><tbody>{queue.map((c,i)=><tr key={c.call_id} className={`border-b last:border-0 ${c.priority===5?"bg-red-50/50":""}`}><td className="p-3 font-bold">{i+1}</td><td className="font-semibold">#{c.call_id}</td><td>{c.emergency_type}</td><td>{c.location}</td><td><PriorityBadge value={c.priority}/></td><td><StatusBadge value={c.status}/></td><td><Link className="text-red-600" to={`/calls/${c.call_id}`}>Process</Link></td></tr>)}{queue.length===0&&<tr><td colSpan="7" className="p-10 text-center text-slate-500">No waiting emergencies</td></tr>}</tbody></table></div>
 <div className="card p-5 text-sm text-slate-600"><b>Algorithm demonstration:</b> If calls are 101→3, 102→5, 103→5, 104→2, 105→4, the backend returns <b>102 → 103 → 105 → 101 → 104</b>.</div>
 </div>
}
