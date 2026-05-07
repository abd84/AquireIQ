import Link from "next/link";
import { ArrowRight, Search, Building2, Zap, TrendingUp, Star, Shield } from "lucide-react";

const features = [
  {
    icon: Search,
    title: "Discovery",
    description: "Searches local business databases across any US city and state. Pulls name, ratings, domain, and contact basics.",
    gradient: "from-blue-500 to-blue-600",
    bg: "bg-blue-50",
    border: "border-blue-100",
  },
  {
    icon: Building2,
    title: "Enrichment",
    description: "Fills data voids using website scraping for founding year and owner info, plus automated executive email discovery.",
    gradient: "from-indigo-500 to-violet-600",
    bg: "bg-indigo-50",
    border: "border-indigo-100",
  },
  {
    icon: Zap,
    title: "AI Scoring",
    description: "Generates a 0–100 Succession Readiness score and custom M&A outreach drafts powered by AI.",
    gradient: "from-violet-500 to-purple-600",
    bg: "bg-violet-50",
    border: "border-violet-100",
  },
];

const scoringPillars = [
  { label: "Financial Fit", pts: 30, color: "bg-blue-500" },
  { label: "Operational Profile", pts: 25, color: "bg-indigo-500" },
  { label: "Owner Exit Signals", pts: 25, color: "bg-violet-500" },
  { label: "Market Positioning", pts: 10, color: "bg-purple-500" },
  { label: "Outreach Priority", pts: 10, color: "bg-pink-500" },
];

const tiers = [
  { label: "Tier 1", sub: "Hot Target", range: "75–100", textColor: "text-emerald-700", bg: "bg-emerald-50", border: "border-emerald-200", dot: "bg-emerald-500" },
  { label: "Tier 2", sub: "Strong Candidate", range: "55–74", textColor: "text-blue-700", bg: "bg-blue-50", border: "border-blue-200", dot: "bg-blue-500" },
  { label: "Tier 3", sub: "Monitor", range: "35–54", textColor: "text-amber-700", bg: "bg-amber-50", border: "border-amber-200", dot: "bg-amber-500" },
  { label: "No Fit", sub: "Below threshold", range: "0–34", textColor: "text-slate-600", bg: "bg-slate-100", border: "border-slate-200", dot: "bg-slate-400" },
];

export default function Home() {
  return (
    <div className="pb-20">
      {/* ── Hero ─────────────────────────────────────────────── */}
      <div className="py-12 sm:py-16 text-center max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 border border-blue-100 mb-8">
          <div className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse" />
          <span className="text-xs font-bold text-blue-700 uppercase tracking-widest">
            Caprae Capital · AI Challenge
          </span>
        </div>

        <h1 className="text-5xl sm:text-6xl font-black tracking-tight text-slate-900 leading-[1.05] mb-6">
          Pre-market SMB{" "}
          <span className="block bg-clip-text text-transparent bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600">
            Deal Sourcing
          </span>
        </h1>

        <p className="text-lg text-slate-500 font-medium leading-relaxed mb-10 max-w-2xl mx-auto">
          Find owner-operated SMBs with aging founders, score them on a proprietary Succession Readiness model,
          and generate M&A-framed outreach — in seconds.
        </p>

        <div className="flex items-center justify-center gap-4 flex-wrap">
          <Link
            href="/search"
            className="inline-flex items-center gap-2.5 px-7 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-sm font-bold shadow-xl shadow-blue-500/25 hover:shadow-blue-500/40 hover:from-blue-700 hover:to-indigo-700 transition-all"
          >
            Start Sourcing
            <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            href="/companies"
            className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-white border border-slate-200 text-slate-700 text-sm font-bold shadow-sm hover:bg-slate-50 hover:border-slate-300 transition-all"
          >
            View Leads
          </Link>
        </div>
      </div>

      {/* ── Pipeline steps ───────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-4">
        {features.map((f) => (
          <div
            key={f.title}
            className={`relative bg-white rounded-2xl border ${f.border} shadow-sm hover:shadow-md transition-shadow p-6 overflow-hidden group`}
          >
            <div className={`absolute -right-4 -top-4 w-20 h-20 rounded-full ${f.bg} opacity-60 group-hover:opacity-100 transition-opacity`} />
            <div className={`relative inline-flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br ${f.gradient} shadow-md mb-4`}>
              <f.icon className="h-5 w-5 text-white" />
            </div>
            <dt className="font-black text-slate-900 text-base mb-1.5">{f.title}</dt>
            <dd className="text-sm text-slate-500 leading-relaxed">{f.description}</dd>
          </div>
        ))}
      </div>

      {/* ── Scoring model ────────────────────────────────────── */}
      <div className="mt-10 bg-white rounded-2xl border border-slate-200/70 shadow-sm overflow-hidden">
        <div className="px-6 py-5 border-b border-slate-100 flex items-center gap-3">
          <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 shadow">
            <TrendingUp className="h-4 w-4 text-white" />
          </div>
          <div>
            <h2 className="font-black text-slate-900 text-base">Succession Readiness Score</h2>
            <p className="text-xs text-slate-500 font-medium">5-category weighted model · 0–100 points</p>
          </div>
        </div>
        <div className="p-6 space-y-3">
          {scoringPillars.map((p) => (
            <div key={p.label} className="flex items-center gap-4">
              <div className="w-40 text-xs font-semibold text-slate-600 flex-shrink-0">{p.label}</div>
              <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                <div className={`h-full rounded-full ${p.color}`} style={{ width: `${p.pts}%` }} />
              </div>
              <div className="w-12 text-right text-xs font-bold text-slate-700">{p.pts} pts</div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Tiers ────────────────────────────────────────────── */}
      <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3">
        {tiers.map((t) => (
          <div key={t.label} className={`rounded-xl border ${t.border} ${t.bg} px-4 py-3.5`}>
            <div className="flex items-center gap-1.5 mb-1">
              <div className={`w-2 h-2 rounded-full ${t.dot}`} />
              <span className={`text-xs font-black ${t.textColor}`}>{t.label}</span>
            </div>
            <p className={`text-xs font-semibold ${t.textColor} opacity-80`}>{t.sub}</p>
            <p className={`text-[11px] font-mono font-bold ${t.textColor} opacity-50 mt-0.5`}>{t.range} pts</p>
          </div>
        ))}
      </div>

      {/* ── Competitive table ────────────────────────────────── */}
      <div className="mt-10 bg-white rounded-2xl border border-slate-200/70 shadow-sm overflow-hidden">
        <div className="px-6 py-5 border-b border-slate-100 flex items-center gap-3">
          <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600 shadow">
            <Shield className="h-4 w-4 text-white" />
          </div>
          <div>
            <h2 className="font-black text-slate-900 text-base">What AcquireIQ Does That Nobody Else Does</h2>
            <p className="text-xs text-slate-500 font-medium">vs. legacy deal-sourcing tools</p>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="bg-slate-50/80 border-b border-slate-100">
                <th className="py-3 pl-6 pr-4 text-left text-[11px] font-bold uppercase tracking-widest text-slate-500">Capability</th>
                {["Tool A", "Tool B", "Tool C", "AcquireIQ"].map((h) => (
                  <th key={h} className={`py-3 px-4 text-center text-[11px] font-bold uppercase tracking-widest ${h === "AcquireIQ" ? "text-blue-600" : "text-slate-500"}`}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50">
              {[
                ["Succession Readiness Score", false, false, false, true],
                ["Silver Tsunami targeting", false, false, false, true],
                ["M&A-framed outreach (not sales)", false, false, false, true],
                ["AI score explanation", false, false, false, true],
                ["Pre-market / off-market SMB focus", false, false, "partial", true],
                ["Affordable for search fund operators", false, false, false, true],
              ].map(([cap, ...vals]) => (
                <tr key={cap as string} className="hover:bg-slate-50/50 transition-colors">
                  <td className="py-3 pl-6 pr-4 text-sm text-slate-700 font-medium">{cap as string}</td>
                  {vals.map((v, i) => (
                    <td key={i} className="py-3 px-4 text-center">
                      {v === true ? (
                        <Star className="h-4 w-4 text-emerald-500 mx-auto fill-emerald-500" />
                      ) : v === "partial" ? (
                        <span className="text-xs font-semibold text-amber-500">Partial</span>
                      ) : (
                        <span className="text-slate-300 font-bold text-base">—</span>
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
