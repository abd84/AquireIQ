import { SearchForm } from "@/components/SearchForm";
import { Target, Zap, Shield } from "lucide-react";

const stats = [
  { label: 'Score categories', value: '5', icon: Target },
  { label: 'AI model', value: 'Proprietary', icon: Zap },
  { label: 'Tier classification', value: 'Instant', icon: Shield },
];

export default function SearchPage() {
  return (
    <div className="pb-16">
      {/* Hero section */}
      <div className="mb-10">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-50 border border-blue-100 mb-5">
          <div className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse" />
          <span className="text-xs font-bold text-blue-700 uppercase tracking-wider">AI Pipeline Ready</span>
        </div>

        <h1 className="text-4xl sm:text-5xl font-black tracking-tight text-slate-900 leading-[1.1] mb-4">
          Find Your Next{' '}
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
            Acquisition
          </span>
        </h1>
        <p className="text-base text-slate-500 font-medium max-w-xl leading-relaxed">
          Describe a business type and location. Our pipeline discovers business candidates,
          enriches them with owner data, and scores each on Succession Readiness in seconds.
        </p>

        {/* Stats row */}
        <div className="flex flex-wrap gap-6 mt-8 mb-8">
          {stats.map((s) => (
            <div key={s.label} className="flex items-center gap-2.5">
              <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-slate-100 border border-slate-200">
                <s.icon className="h-4 w-4 text-slate-600" />
              </div>
              <div>
                <p className="text-sm font-black text-slate-900">{s.value}</p>
                <p className="text-[11px] text-slate-500 font-medium">{s.label}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Form */}
      <SearchForm />
    </div>
  );
}
