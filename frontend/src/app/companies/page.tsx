'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { ScoreBadge } from '@/components/ScoreBadge';
import { apiUrl } from '@/lib/utils';
import {
  Building2,
  ExternalLink,
  Activity,
  ArrowRight,
  Users,
  MapPin,
  DollarSign,
  Mail,
} from 'lucide-react';
import { motion } from 'framer-motion';

type Company = {
  id: string;
  name: string;
  domain?: string;
  hq_city?: string;
  hq_state?: string;
  revenue_estimate_low?: number;
  revenue_estimate_high?: number;
  acquisition_score?: number;
  score_tier?: string;
  enrichment_status: string;
  owner_name?: string;
  owner_email?: string;
  industry_description?: string;
};

function formatRevenue(low?: number, high?: number) {
  if (!low && !high) return null;
  const fmt = (n: number) => `$${(n / 1_000_000).toFixed(1)}M`;
  if (low && high) return `${fmt(low)} – ${fmt(high)}`;
  return low ? fmt(low) : high ? fmt(high!) : null;
}

export default function CompaniesPage() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const res = await fetch(apiUrl('/api/companies'));
        if (res.ok) setCompanies(await res.json());
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchCompanies();
    const interval = setInterval(fetchCompanies, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-black tracking-tight text-slate-900">
            Company Leads
          </h1>
          <p className="mt-1 text-sm text-slate-500 font-medium">
            {companies.length > 0
              ? `${companies.length} target${companies.length !== 1 ? 's' : ''} · sorted by Succession Readiness score`
              : 'Pre-qualified M&A targets scored by AI'}
          </p>
        </div>
        <Link
          href="/search"
          className="hidden sm:inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-sm font-bold text-white shadow-md shadow-blue-500/20 hover:shadow-blue-500/35 transition-shadow"
        >
          New Search
          <ArrowRight className="h-4 w-4" />
        </Link>
      </div>

      {/* Table card */}
      <div className="bg-white rounded-2xl border border-slate-200/70 shadow-xl shadow-slate-200/50 overflow-hidden">
        {/* Table top accent */}
        <div className="h-0.5 bg-gradient-to-r from-blue-500 via-indigo-500 to-violet-500" />

        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="border-b border-slate-100 bg-slate-50/80">
                <th className="py-3.5 pl-6 pr-3 text-left text-[11px] font-bold uppercase tracking-widest text-slate-500">
                  Company
                </th>
                <th className="px-4 py-3.5 text-left text-[11px] font-bold uppercase tracking-widest text-slate-500">
                  <span className="flex items-center gap-1.5"><MapPin className="h-3 w-3" />Location</span>
                </th>
                <th className="px-4 py-3.5 text-left text-[11px] font-bold uppercase tracking-widest text-slate-500">
                  <span className="flex items-center gap-1.5"><DollarSign className="h-3 w-3" />Revenue</span>
                </th>
                <th className="px-4 py-3.5 text-left text-[11px] font-bold uppercase tracking-widest text-slate-500">
                  Score
                </th>
                <th className="px-4 py-3.5 text-left text-[11px] font-bold uppercase tracking-widest text-slate-500">
                  Status
                </th>
                <th className="py-3.5 pl-3 pr-6 text-right text-[11px] font-bold uppercase tracking-widest text-slate-500">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr>
                  <td colSpan={6} className="py-20 text-center">
                    <Activity className="h-6 w-6 animate-spin text-blue-500 mx-auto mb-3" />
                    <p className="text-sm font-medium text-slate-500">Loading companies...</p>
                  </td>
                </tr>
              ) : companies.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-20 text-center">
                    <div className="flex flex-col items-center gap-3">
                      <div className="w-12 h-12 rounded-2xl bg-slate-100 flex items-center justify-center">
                        <Users className="h-6 w-6 text-slate-400" />
                      </div>
                      <p className="text-sm font-semibold text-slate-600">No leads yet</p>
                      <p className="text-xs text-slate-400">Run a Sourcing Search to discover targets</p>
                      <Link
                        href="/search"
                        className="mt-1 inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-blue-600 text-white text-xs font-bold shadow-sm hover:bg-blue-700 transition-colors"
                      >
                        Start searching
                        <ArrowRight className="h-3.5 w-3.5" />
                      </Link>
                    </div>
                  </td>
                </tr>
              ) : (
                companies.map((company, i) => {
                  const revenue = formatRevenue(company.revenue_estimate_low, company.revenue_estimate_high);
                  return (
                    <motion.tr
                      key={company.id}
                      initial={{ opacity: 0, y: 6 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.04, duration: 0.3 }}
                      className="group hover:bg-slate-50/70 transition-colors"
                    >
                      {/* Company */}
                      <td className="py-4 pl-6 pr-3">
                        <div className="flex items-center gap-3">
                          <div className="h-10 w-10 flex-shrink-0 flex items-center justify-center bg-gradient-to-br from-slate-100 to-slate-200 rounded-xl border border-slate-200/60 group-hover:border-blue-100 group-hover:from-blue-50 group-hover:to-indigo-50 transition-all">
                            <Building2 className="h-5 w-5 text-slate-500 group-hover:text-blue-500 transition-colors" />
                          </div>
                          <div className="min-w-0">
                            <div className="flex items-center gap-2">
                              <Link
                                href={`/companies/${company.id}`}
                                className="font-bold text-slate-900 text-sm hover:text-blue-600 transition-colors truncate max-w-[180px]"
                              >
                                {company.name}
                              </Link>
                              {company.domain && (
                                <a
                                  href={`https://${company.domain}`}
                                  target="_blank"
                                  rel="noreferrer"
                                  className="flex-shrink-0"
                                >
                                  <ExternalLink className="h-3.5 w-3.5 text-slate-300 hover:text-blue-500 transition-colors" />
                                </a>
                              )}
                            </div>
                            <p className="text-xs text-slate-500 mt-0.5 truncate max-w-[200px]">
                              {company.owner_name
                                ? <span className="text-indigo-600 font-medium">{company.owner_name}</span>
                                : company.industry_description || 'Unknown Industry'}
                            </p>
                          </div>
                        </div>
                      </td>

                      {/* Location */}
                      <td className="px-4 py-4">
                        <span className="text-sm text-slate-600 font-medium">
                          {company.hq_city && company.hq_state
                            ? `${company.hq_city}, ${company.hq_state}`
                            : <span className="text-slate-300">—</span>}
                        </span>
                      </td>

                      {/* Revenue */}
                      <td className="px-4 py-4">
                        {revenue ? (
                          <span className="text-sm font-semibold text-slate-700">{revenue}</span>
                        ) : (
                          <span className="text-slate-300 text-sm">—</span>
                        )}
                      </td>

                      {/* Score */}
                      <td className="px-4 py-4">
                        <ScoreBadge score={company.acquisition_score} tier={company.score_tier} />
                      </td>

                      {/* Status */}
                      <td className="px-4 py-4">
                        {company.enrichment_status === 'enriching' ? (
                          <span className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-bold text-amber-700 bg-amber-50 border border-amber-100">
                            <Activity className="h-3 w-3 animate-spin" />
                            Processing
                          </span>
                        ) : company.enrichment_status === 'complete' ? (
                          <span className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-100">
                            <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                            Ready
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-bold text-slate-600 bg-slate-100 border border-slate-200">
                            {company.enrichment_status}
                          </span>
                        )}
                      </td>

                      {/* Actions */}
                      <td className="py-4 pl-3 pr-6">
                        <div className="flex items-center justify-end gap-1">
                          {company.owner_email && (
                            <Link
                              href="/outreach"
                              className="p-2 rounded-lg text-slate-400 hover:text-blue-600 hover:bg-blue-50 transition-all"
                              title="Outreach queue"
                            >
                              <Mail className="h-4 w-4" />
                            </Link>
                          )}
                          <Link
                            href={`/companies/${company.id}`}
                            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-100 transition-all"
                          >
                            View <ArrowRight className="h-3.5 w-3.5" />
                          </Link>
                        </div>
                      </td>
                    </motion.tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
