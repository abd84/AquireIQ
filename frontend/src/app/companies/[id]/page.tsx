'use client';

import { use, useEffect, useState } from 'react';
import { ScoreBadge } from '@/components/ScoreBadge';
import { apiUrl } from '@/lib/utils';
import {
  Building2, Mail, ExternalLink, MapPin, Phone, Users,
  Briefcase, ChevronLeft, Star, TrendingUp, Brain, Send,
  CheckCircle2, Copy, Calendar,
} from 'lucide-react';
import Link from 'next/link';
import { motion } from 'framer-motion';

// ── Score metadata ──────────────────────────────────────────────
const SCORE_META: Record<string, { label: string; max: number; color: string; bar: string }> = {
  financial_fit:       { label: 'Financial Fit',       max: 30, color: 'text-blue-700',   bar: 'bg-blue-500' },
  operational_profile: { label: 'Operational Profile', max: 25, color: 'text-indigo-700', bar: 'bg-indigo-500' },
  owner_exit_signals:  { label: 'Owner Exit Signals',  max: 25, color: 'text-violet-700', bar: 'bg-violet-500' },
  market_positioning:  { label: 'Market Positioning',  max: 10, color: 'text-purple-700', bar: 'bg-purple-500' },
  outreach_priority:   { label: 'Outreach Priority',   max: 10, color: 'text-pink-700',   bar: 'bg-pink-500' },
};

// ── Highlight AI analysis text ───────────────────────────────────
function HighlightedAnalysis({ text }: { text: string }) {
  const paragraphs = text.split(/\n+/).filter(Boolean);

  const PATTERNS: { re: RegExp; cls: string }[] = [
    { re: /\b\d{2,3}\/100\b|\b\d{2,3}\s*out\s*of\s*100\b/gi,
      cls: 'bg-blue-100 text-blue-800 font-bold px-1 rounded' },
    { re: /\bTier\s*[123]\b|Hot Target|Strong Fit|Strong Candidate/gi,
      cls: 'bg-emerald-100 text-emerald-800 font-bold px-1 rounded' },
    { re: /\b\d{2,3}\s*(?:years?|yr)\b|est(?:ablished)?\s+(?:in\s+)?\d{4}|founded\s+(?:in\s+)?\d{4}|since\s+\d{4}/gi,
      cls: 'bg-amber-100 text-amber-800 font-semibold px-1 rounded' },
    { re: /\$[\d,.]+[MBK]?(?:\s*(?:–|-|to)\s*\$[\d,.]+[MBK]?)?/gi,
      cls: 'bg-violet-100 text-violet-800 font-semibold px-1 rounded' },
    { re: /\b(?:strong|excellent|favorable|high|significant|robust|well-positioned|prime|ideal|compelling|substantial)\b/gi,
      cls: 'text-emerald-700 font-semibold' },
    { re: /\b(?:limited|low|concern|risk|weak|minimal|lack|absence|gap)\b/gi,
      cls: 'text-amber-600 font-semibold' },
    { re: /\b(?:succession|exit|acquisition|retire(?:ment)?|transition|owner-operator|key[- ]man)\b/gi,
      cls: 'text-indigo-700 font-semibold underline decoration-dotted decoration-indigo-400' },
  ];

  function applyHighlights(raw: string): React.ReactNode[] {
    type Span = { start: number; end: number; cls: string };
    const spans: Span[] = [];
    for (const { re, cls } of PATTERNS) {
      re.lastIndex = 0;
      let m: RegExpExecArray | null;
      while ((m = re.exec(raw)) !== null) {
        const overlaps = spans.some(s => m!.index < s.end && m!.index + m![0].length > s.start);
        if (!overlaps) spans.push({ start: m.index, end: m.index + m[0].length, cls });
      }
    }
    spans.sort((a, b) => a.start - b.start);
    const nodes: React.ReactNode[] = [];
    let cursor = 0;
    spans.forEach(({ start, end, cls }, i) => {
      if (cursor < start) nodes.push(raw.slice(cursor, start));
      nodes.push(<mark key={i} className={`not-italic bg-transparent ${cls}`}>{raw.slice(start, end)}</mark>);
      cursor = end;
    });
    if (cursor < raw.length) nodes.push(raw.slice(cursor));
    return nodes;
  }

  return (
    <div className="space-y-4">
      {paragraphs.map((para, i) => (
        <p key={i} className="text-sm text-slate-700 leading-relaxed">{applyHighlights(para)}</p>
      ))}
    </div>
  );
}

// ── Main page ────────────────────────────────────────────────────
export default function CompanyDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [company, setCompany] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [queuing, setQueuing] = useState(false);
  const [queued, setQueued] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    fetch(apiUrl(`/api/companies/${id}`))
      .then(r => r.ok ? r.json() : null)
      .then(d => { setCompany(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [id]);

  const handleQueueOutreach = async () => {
    setQueuing(true);
    try {
      const res = await fetch(apiUrl(`/api/outreach/${company.id}/queue`), { method: 'POST' });
      if (res.ok) setQueued(true);
    } catch (err) { console.error(err); }
    finally { setQueuing(false); }
  };

  const handleCopyEmail = () => {
    if (company?.outreach_body) {
      navigator.clipboard.writeText(`Subject: ${company.outreach_subject}\n\n${company.outreach_body}`);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (loading) return (
    <div className="flex items-center justify-center py-24">
      <div className="h-6 w-6 rounded-full border-2 border-blue-500 border-t-transparent animate-spin" />
    </div>
  );
  if (!company) return <div className="py-10 text-center text-slate-500">Company not found.</div>;

  const tierGradient: Record<string, string> = {
    'Tier 1': 'from-emerald-500 to-teal-600',
    'Tier 2': 'from-blue-500 to-indigo-600',
    'Tier 3': 'from-amber-500 to-orange-600',
    'No Fit': 'from-slate-400 to-slate-500',
  };
  const headerGradient = tierGradient[company.score_tier] ?? 'from-slate-400 to-slate-500';
  const businessAge = company.founded_year ? new Date().getFullYear() - company.founded_year : null;

  return (
    <div className="pb-16">
      <div className="mb-5">
        <Link href="/companies" className="inline-flex items-center gap-1 text-sm font-semibold text-slate-500 hover:text-blue-600 transition-colors">
          <ChevronLeft className="h-4 w-4" /> Back to Leads
        </Link>
      </div>

      {/* Hero header card */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
        className="relative bg-white rounded-2xl border border-slate-200/70 shadow-xl shadow-slate-200/50 overflow-hidden mb-6">
        <div className={`h-1 bg-gradient-to-r ${headerGradient}`} />
        <div className="p-6 sm:p-8">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className={`h-14 w-14 flex-shrink-0 flex items-center justify-center rounded-2xl bg-gradient-to-br ${headerGradient} shadow-lg`}>
                <Building2 className="h-7 w-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-black tracking-tight text-slate-900">{company.name}</h1>
                <div className="flex items-center gap-2 mt-1 flex-wrap">
                  <span className="text-sm text-slate-500 font-medium">{company.industry_description || 'Unknown Industry'}</span>
                  {company.domain && (
                    <a href={`https://${company.domain}`} target="_blank" rel="noreferrer"
                      className="inline-flex items-center gap-1 text-xs font-semibold text-blue-600 hover:text-blue-700 transition-colors">
                      {company.domain} <ExternalLink className="h-3 w-3" />
                    </a>
                  )}
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3 flex-shrink-0">
              <ScoreBadge score={company.acquisition_score} tier={company.score_tier} />
              {company.owner_email && (
                <button onClick={handleQueueOutreach} disabled={queuing || queued}
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-sm font-bold text-white shadow-md shadow-blue-500/25 hover:shadow-blue-500/40 disabled:opacity-60 disabled:cursor-not-allowed transition-all">
                  {queued ? <CheckCircle2 className="h-4 w-4" /> : <Mail className="h-4 w-4" />}
                  {queuing ? 'Queuing…' : queued ? 'Queued' : 'Queue Outreach'}
                </button>
              )}
            </div>
          </div>

          {/* Quick-stat pills */}
          <div className="flex flex-wrap gap-2 mt-5">
            {company.hq_city && company.hq_state && (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 text-xs font-semibold text-slate-700">
                <MapPin className="h-3 w-3 text-slate-400" />{company.hq_city}, {company.hq_state}
              </span>
            )}
            {businessAge && (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 border border-amber-200 text-xs font-bold text-amber-700">
                <Briefcase className="h-3 w-3" />{businessAge} yrs in business
              </span>
            )}
            {company.google_rating && (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-yellow-50 border border-yellow-200 text-xs font-bold text-yellow-700">
                <Star className="h-3 w-3 fill-yellow-500 text-yellow-500" />
                {company.google_rating} · {company.google_review_count} reviews
              </span>
            )}
            {company.revenue_estimate_low && (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-xs font-bold text-emerald-700">
                <TrendingUp className="h-3 w-3" />
                ${(company.revenue_estimate_low / 1_000_000).toFixed(1)}M – ${(company.revenue_estimate_high / 1_000_000).toFixed(1)}M est.
              </span>
            )}
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* LEFT COLUMN */}
        <div className="lg:col-span-2 space-y-6">

          {/* Score Breakdown with progress bars */}
          {company.score_breakdown && (
            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }}
              className="bg-white rounded-2xl border border-slate-200/70 shadow-sm overflow-hidden">
              <div className="px-6 py-4 border-b border-slate-100 flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center shadow">
                  <TrendingUp className="h-4 w-4 text-white" />
                </div>
                <h2 className="font-black text-slate-900">Score Breakdown</h2>
              </div>
              <div className="p-6 space-y-5">
                {Object.entries(company.score_breakdown as Record<string, number>).map(([key, val]) => {
                  const meta = SCORE_META[key];
                  if (!meta) return null;
                  const pct = Math.round((val / meta.max) * 100);
                  return (
                    <div key={key}>
                      <div className="flex items-center justify-between mb-1.5">
                        <span className={`text-xs font-bold uppercase tracking-widest ${meta.color}`}>{meta.label}</span>
                        <span className="text-sm font-black text-slate-800">
                          {val} <span className="text-slate-400 font-medium text-xs">/ {meta.max}</span>
                        </span>
                      </div>
                      <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${pct}%` }}
                          transition={{ duration: 0.7, ease: 'easeOut', delay: 0.1 }}
                          className={`h-full rounded-full ${meta.bar}`}
                        />
                      </div>
                    </div>
                  );
                })}
                <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-sm font-bold text-slate-600">Total Score</span>
                  <span className="text-2xl font-black text-blue-700">
                    {company.acquisition_score}
                    <span className="text-base text-slate-400 font-medium"> / 100</span>
                  </span>
                </div>
              </div>
            </motion.div>
          )}

          {/* AI Succession Analysis */}
          <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            className="bg-white rounded-2xl border border-slate-200/70 shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-100 flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-600 to-purple-600 flex items-center justify-center shadow">
                <Brain className="h-4 w-4 text-white" />
              </div>
              <div>
                <h2 className="font-black text-slate-900">AI Succession Analysis</h2>
                {company.score_explanation && (
                  <p className="text-[11px] text-slate-400 font-medium mt-0.5">Key terms are highlighted below</p>
                )}
              </div>
            </div>
            <div className="p-6">
              {company.score_explanation ? (
                <>
                  {/* Legend */}
                  <div className="flex flex-wrap gap-2 mb-5 pb-4 border-b border-slate-100">
                    {[
                      { cls: 'bg-blue-100 text-blue-800', label: 'Score' },
                      { cls: 'bg-emerald-100 text-emerald-800', label: 'Tier / Signal' },
                      { cls: 'bg-amber-100 text-amber-800', label: 'Age / Date' },
                      { cls: 'bg-violet-100 text-violet-800', label: 'Revenue' },
                      { cls: 'text-emerald-700 font-semibold', label: '↑ Positive' },
                      { cls: 'text-amber-600 font-semibold', label: '↓ Caution' },
                      { cls: 'text-indigo-700 underline decoration-dotted', label: 'M&A Term' },
                    ].map(({ cls, label }) => (
                      <span key={label} className={`text-[10px] font-bold px-2 py-0.5 rounded border border-slate-200 bg-white ${cls}`}>
                        {label}
                      </span>
                    ))}
                  </div>
                  <HighlightedAnalysis text={company.score_explanation} />
                </>
              ) : (
                <div className="flex items-center gap-3 p-4 rounded-xl bg-slate-50 border border-slate-200">
                  <Brain className="h-5 w-5 text-slate-300 flex-shrink-0" />
                  <p className="text-sm text-slate-500">
                    AI analysis is generated for <span className="font-semibold text-slate-700">Tier 1</span> and{' '}
                    <span className="font-semibold text-slate-700">Tier 2</span> targets only.
                  </p>
                </div>
              )}
            </div>
          </motion.div>

          {/* Draft Outreach Email */}
          {company.outreach_body && (
            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}
              className="bg-white rounded-2xl border border-slate-200/70 shadow-sm overflow-hidden">
              <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-blue-600 flex items-center justify-center shadow">
                    <Send className="h-4 w-4 text-white" />
                  </div>
                  <h2 className="font-black text-slate-900">AI Draft Outreach Email</h2>
                </div>
                <button onClick={handleCopyEmail}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 transition-colors">
                  {copied ? <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> : <Copy className="h-3.5 w-3.5" />}
                  {copied ? 'Copied!' : 'Copy'}
                </button>
              </div>
              <div className="p-6">
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 mb-4 space-y-2">
                  <div className="flex items-center gap-3">
                    <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 w-14">To</span>
                    <span className="text-sm font-semibold text-slate-700">{company.owner_email}</span>
                  </div>
                  <div className="flex items-start gap-3">
                    <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 w-14 pt-0.5">Subject</span>
                    <span className="text-sm font-bold text-slate-900">{company.outreach_subject}</span>
                  </div>
                </div>
                <div className="bg-white border border-slate-200 rounded-xl p-5 text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">
                  {company.outreach_body}
                </div>
                {!queued && company.owner_email && (
                  <div className="mt-4 flex items-center justify-between p-3 rounded-xl bg-blue-50 border border-blue-100">
                    <div className="flex items-center gap-2">
                      <Calendar className="h-4 w-4 text-blue-500" />
                      <span className="text-xs font-semibold text-blue-700">Ready to send via outreach pipeline</span>
                    </div>
                    <button onClick={handleQueueOutreach} disabled={queuing}
                      className="text-xs font-bold text-blue-700 hover:text-blue-900 transition-colors">
                      {queuing ? 'Queuing…' : 'Queue now →'}
                    </button>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </div>

        {/* RIGHT COLUMN */}
        <div className="space-y-6">
          <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.12 }}
            className="bg-white rounded-2xl border border-slate-200/70 shadow-sm overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100">
              <h2 className="font-black text-slate-900 text-sm">Business Overview</h2>
            </div>
            <div className="p-5 space-y-4">
              {[
                { icon: MapPin,    label: 'Location',     value: company.hq_city && company.hq_state ? `${company.hq_city}, ${company.hq_state}` : null },
                { icon: Phone,     label: 'Phone',        value: company.phone },
                { icon: Briefcase, label: 'Founded',      value: company.founded_year ? `${company.founded_year} · ${businessAge} yrs old` : null },
                { icon: Users,     label: 'Employees',    value: company.employee_count_low ? `${company.employee_count_low} – ${company.employee_count_high}` : null },
                { icon: Star,      label: 'Google Rating',value: company.google_rating ? `${company.google_rating} ★  (${company.google_review_count} reviews)` : null },
              ].map(({ icon: Icon, label, value }) => (
                <div key={label} className="flex items-start gap-3">
                  <div className="w-7 h-7 rounded-lg bg-slate-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <Icon className="h-3.5 w-3.5 text-slate-500" />
                  </div>
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400">{label}</p>
                    <p className={`text-sm font-semibold mt-0.5 ${value ? 'text-slate-800' : 'text-slate-300'}`}>{value ?? 'Unknown'}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.16 }}
            className="bg-white rounded-2xl border border-slate-200/70 shadow-sm overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100">
              <h2 className="font-black text-slate-900 text-sm">Key Contact</h2>
            </div>
            <div className="p-5 space-y-4">
              <div className="flex items-start gap-3">
                <div className="w-7 h-7 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center flex-shrink-0">
                  <Users className="h-3.5 w-3.5 text-indigo-500" />
                </div>
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Name</p>
                  <p className={`text-sm font-semibold mt-0.5 ${company.owner_name ? 'text-slate-800' : 'text-slate-300'}`}>
                    {company.owner_name || 'Not Identified'}
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="w-7 h-7 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center flex-shrink-0">
                  <Mail className="h-3.5 w-3.5 text-indigo-500" />
                </div>
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Email</p>
                  {company.owner_email ? (
                    <a href={`mailto:${company.owner_email}`}
                      className="text-sm font-semibold mt-0.5 text-indigo-600 hover:text-indigo-800 break-all transition-colors">
                      {company.owner_email}
                    </a>
                  ) : (
                    <p className="text-sm font-semibold mt-0.5 text-slate-300">Not Extracted</p>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
