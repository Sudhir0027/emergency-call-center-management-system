export default function StatCard({title,value,icon:Icon, tone="slate"}) {
  const tones={red:"text-red-600 bg-red-50",amber:"text-amber-600 bg-amber-50",blue:"text-blue-600 bg-blue-50",green:"text-emerald-600 bg-emerald-50",slate:"text-slate-600 bg-slate-100"};
  return <div className="card p-4"><div className="flex justify-between items-start"><div><p className="text-xs uppercase tracking-wide text-slate-500">{title}</p><p className="text-2xl font-bold text-slate-900 mt-2">{value}</p></div><div className={`p-2.5 rounded-xl ${tones[tone]}`}><Icon size={20}/></div></div></div>;
}
