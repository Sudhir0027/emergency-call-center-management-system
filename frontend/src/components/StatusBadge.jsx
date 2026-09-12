const map={WAITING:"bg-amber-100 text-amber-700",ASSIGNED:"bg-blue-100 text-blue-700",IN_PROGRESS:"bg-violet-100 text-violet-700",RESOLVED:"bg-emerald-100 text-emerald-700",CANCELLED:"bg-slate-100 text-slate-500"};
export default function StatusBadge({value}){return <span className={`px-2 py-1 rounded-full text-xs font-semibold ${map[value]||""}`}>{value.replace("_"," ")}</span>}
