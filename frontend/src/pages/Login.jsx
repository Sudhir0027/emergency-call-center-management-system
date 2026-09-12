import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { ShieldAlert } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { messageOf } from "../services/api";

export default function Login(){
 const {user,login}=useAuth(); const nav=useNavigate(); const [username,setUsername]=useState("operator"); const [password,setPassword]=useState("Operator@123"); const [error,setError]=useState(""); const [busy,setBusy]=useState(false);
 if(user)return <Navigate to="/" replace/>;
 const submit=async e=>{e.preventDefault();setError("");setBusy(true);try{await login(username,password);nav("/")}catch(err){setError(messageOf(err))}finally{setBusy(false)}};
 return <div className="min-h-screen bg-slate-950 grid place-items-center p-4"><form onSubmit={submit} className="w-full max-w-md bg-white rounded-3xl p-8 shadow-2xl">
  <div className="flex items-center gap-3 mb-8"><div className="p-3 bg-red-50 text-red-600 rounded-xl"><ShieldAlert/></div><div><h1 className="text-2xl font-bold">Emergency Control</h1><p className="text-sm text-slate-500">Secure operator login</p></div></div>
  {error&&<div className="mb-4 p-3 rounded-lg bg-red-50 text-red-700 text-sm">{error}</div>}
  <label className="text-sm font-medium">Username / Email</label><input className="w-full border rounded-xl p-3 mt-1 mb-4" value={username} onChange={e=>setUsername(e.target.value)}/>
  <label className="text-sm font-medium">Password</label><input type="password" className="w-full border rounded-xl p-3 mt-1 mb-6" value={password} onChange={e=>setPassword(e.target.value)}/>
  <button disabled={busy} className="w-full bg-red-600 hover:bg-red-700 text-white py-3 rounded-xl font-semibold disabled:opacity-50">{busy?"Signing in...":"Login"}</button>
  <p className="text-xs text-slate-400 mt-5 text-center">Demo: operator / Operator@123 · admin / Admin@123</p>
 </form></div>
}
