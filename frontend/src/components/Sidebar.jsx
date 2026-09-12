import { NavLink } from "react-router-dom";
import { LayoutDashboard, PhoneCall, ListOrdered, Users, History, Siren, LogOut } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Sidebar() {
  const { user, logout } = useAuth();
  const links = [
    ["/", "Dashboard", LayoutDashboard],
    ["/calls", "Emergency Calls", PhoneCall],
    ["/queue", "Priority Queue", ListOrdered],
    ["/responders", "Responders", Users],
    ["/history", "History", History],
  ];
  return <aside className="w-64 shrink-0 bg-slate-950 text-white min-h-screen hidden md:flex flex-col">
    <div className="p-5 border-b border-slate-800">
      <div className="flex items-center gap-3"><Siren className="text-red-400"/><div><b>Emergency CC</b><p className="text-xs text-slate-400">Operations Center</p></div></div>
    </div>
    <nav className="p-3 space-y-1 flex-1">
      {links.map(([to,label,Icon]) => <NavLink key={to} to={to} end={to==="/"} className={({isActive}) => `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm ${isActive?"bg-red-500/15 text-red-300":"text-slate-300 hover:bg-slate-900"}`}><Icon size={18}/>{label}</NavLink>)}
      {user?.role === "ADMIN" && <div className="px-3 py-5 text-xs text-slate-500 uppercase">Admin controls enabled</div>}
    </nav>
    <button onClick={logout} className="m-3 flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-slate-900 text-slate-300"><LogOut size={18}/> Logout</button>
  </aside>;
}
