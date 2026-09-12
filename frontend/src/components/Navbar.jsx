import { Menu, Radio } from "lucide-react";
import { useAuth } from "../context/AuthContext";
export default function Navbar() {
  const { user } = useAuth();
  return <header className="h-16 bg-white border-b flex items-center justify-between px-5">
    <div className="flex items-center gap-3"><Menu className="md:hidden"/><div><h1 className="font-semibold text-slate-800">Emergency Operations</h1><p className="text-xs text-slate-500">Priority dispatch control center</p></div></div>
    <div className="flex items-center gap-3"><span className="flex items-center gap-1.5 text-xs text-emerald-600"><Radio size={14}/> System online</span><span className="text-sm font-medium text-slate-700">{user?.username}</span><span className="text-[10px] px-2 py-1 rounded-full bg-slate-100">{user?.role}</span></div>
  </header>;
}
