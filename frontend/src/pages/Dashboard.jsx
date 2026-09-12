import { useEffect,useState } from "react";
import { Activity, AlertTriangle, CheckCircle, Clock3, Users, PhoneCall } from "lucide-react";
import api from "../services/api";
import StatCard from "../components/StatCard";
import CallTable from "../components/CallTable";
import PriorityBadge from "../components/PriorityBadge";

export default function Dashboard(){
 const [stats,setStats]=useState({});const[calls,setCalls]=useState([]);const[queue,setQueue]=useState([]);const[dist,setDist]=useState([]);
 const load=async()=>{const [s,c,q,d]=await Promise.all([api.get("/dashboard/stats"),api.get("/dashboard/recent-calls"),api.get("/calls/queue"),api.get("/dashboard/emergency-distribution")]);setStats(s.data);setCalls(c.data);setQueue(q.data);setDist(d.data)};
 useEffect(()=>{load();const t=setInterval(load,5000);return()=>clearInterval(t)},[]);
 return <div className="space-y-6">
  <div><h2 className="text-2xl font-bold">Control Center</h2><p className="text-slate-500 text-sm">Live overview of emergency operations</p></div>
  <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
   <StatCard title="Total Calls" value={stats.total_calls??0} icon={PhoneCall} tone="blue"/><StatCard title="Waiting" value={stats.waiting_calls??0} icon={Clock3} tone="amber"/><StatCard title="Active" value={stats.active_calls??0} icon={Activity} tone="red"/><StatCard title="Resolved" value={stats.resolved_calls??0} icon={CheckCircle} tone="green"/>
  </div>
  <div className="grid lg:grid-cols-3 gap-5">
   <div className="card p-5 lg:col-span-2"><div className="flex justify-between mb-4"><div><h3 className="font-semibold">Priority Queue</h3><p className="text-xs text-slate-500">Highest priority first, lower Call ID breaks ties</p></div><AlertTriangle className="text-red-500"/></div><CallTable calls={queue.slice(0,6)}/></div>
   <div className="card p-5"><h3 className="font-semibold mb-4">Responder Availability</h3><div className="space-y-3"><div className="flex justify-between"><span>Available</span><b className="text-emerald-600">{stats.available_responders??0}</b></div><div className="flex justify-between"><span>Busy</span><b className="text-amber-600">{stats.busy_responders??0}</b></div><div className="flex justify-between"><span>Offline</span><b className="text-slate-500">{stats.offline_responders??0}</b></div><div className="border-t pt-3 flex justify-between"><span>Critical active</span><b className="text-red-600">{stats.critical_emergencies??0}</b></div></div>
   <h3 className="font-semibold mt-8 mb-3">Emergency Distribution</h3><div className="space-y-2">{dist.map(x=><div key={x.type} className="flex items-center gap-2 text-xs"><span className="w-28 truncate">{x.type}</span><div className="h-2 bg-slate-100 rounded flex-1"><div className="h-2 bg-red-500 rounded" style={{width:`${Math.min(100,x.count*12)}%`}}/></div><b>{x.count}</b></div>)}</div>
   </div>
  </div>
  <div className="card p-5"><h3 className="font-semibold mb-4">Recent Calls</h3><CallTable calls={calls}/></div>
 </div>
}
