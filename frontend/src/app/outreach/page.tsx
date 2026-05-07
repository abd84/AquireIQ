'use client';

import { useEffect, useState } from 'react';
import { Mail, Calendar, CheckCircle2, Clock, Inbox } from 'lucide-react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { apiUrl } from '@/lib/utils';

type OutreachLog = {
  id: string;
  company_id: string;
  contact_email: string;
  sequence_stage: number;
  status: string;
  next_touch_date: string;
};

const STAGE_LABELS: Record<number, string> = {
  1: 'Day 0 · Intro',
  2: 'Day 7 · Follow-up',
  3: 'Day 21 · Final touch',
};

export default function OutreachQueuePage() {
  const [logs, setLogs] = useState<OutreachLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch_ = async () => {
      try {
        const res = await fetch(apiUrl('/api/outreach'));
        if (res.ok) setLogs(await res.json());
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetch_();
  }, []);

  const markSent = async (id: string) => {
    try {
      await fetch(apiUrl(`/api/outreach/${id}/mark-sent`), { method: 'PATCH' });
      setLogs(logs.map((l) => (l.id === id ? { ...l, status: 'sent' } : l)));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="pb-16">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-black tracking-tight text-slate-900">Outreach Queue</h1>
        <p className="mt-1 text-sm text-slate-500 font-medium max-w-2xl">
          AI-crafted M&A succession planning emails. Mark contacts as sent to track your sequencing pipeline.
        </p>
      </div>

      {/* Main card */}
      <div className="bg-white rounded-2xl border border-slate-200/70 shadow-xl shadow-slate-200/50 overflow-hidden">
        <div className="h-0.5 bg-gradient-to-r from-indigo-500 via-violet-500 to-purple-500" />

        {loading ? (
          <div className="py-20 text-center">
            <Clock className="h-6 w-6 animate-spin text-indigo-400 mx-auto mb-3" />
            <p className="text-sm font-medium text-slate-500">Loading queue…</p>
          </div>
        ) : logs.length === 0 ? (
          <div className="py-24 text-center">
            <div className="flex flex-col items-center gap-4">
              <div className="w-16 h-16 rounded-2xl bg-slate-100 flex items-center justify-center">
                <Inbox className="h-8 w-8 text-slate-300" />
              </div>
              <div>
                <p className="font-bold text-slate-700 text-base">Queue is empty</p>
                <p className="text-sm text-slate-400 mt-1">
                  Use the{' '}
                  <Link href="/search" className="text-indigo-600 font-semibold hover:underline">
                    Sourcing Search
                  </Link>{' '}
                  to discover targets and queue outreach from a company detail page.
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="border-b border-slate-100 bg-slate-50/80">
                  <th className="py-3.5 pl-6 pr-4 text-left text-[11px] font-bold uppercase tracking-widest text-slate-500">Contact</th>
                  <th className="px-4 py-3.5 text-left text-[11px] font-bold uppercase tracking-widest text-slate-500">Company</th>
                  <th className="px-4 py-3.5 text-left text-[11px] font-bold uppercase tracking-widest text-slate-500">Sequence</th>
                  <th className="px-4 py-3.5 text-left text-[11px] font-bold uppercase tracking-widest text-slate-500">Status</th>
                  <th className="px-4 py-3.5 text-left text-[11px] font-bold uppercase tracking-widest text-slate-500">Next Touch</th>
                  <th className="py-3.5 pl-4 pr-6 text-right text-[11px] font-bold uppercase tracking-widest text-slate-500">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {logs.map((log, i) => (
                  <motion.tr
                    key={log.id}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.05 }}
                    className="hover:bg-slate-50/70 transition-colors"
                  >
                    <td className="py-4 pl-6 pr-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center flex-shrink-0">
                          <Mail className="h-4 w-4 text-indigo-500" />
                        </div>
                        <span className="text-sm font-semibold text-slate-800">
                          {log.contact_email || 'No email found'}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-4">
                      <Link
                        href={`/companies/${log.company_id}`}
                        className="text-sm font-semibold text-indigo-600 hover:text-indigo-800 hover:underline transition-colors"
                      >
                        View Company →
                      </Link>
                    </td>
                    <td className="px-4 py-4">
                      <span className="text-xs font-semibold text-slate-600 bg-slate-100 border border-slate-200 rounded-lg px-2.5 py-1">
                        {STAGE_LABELS[log.sequence_stage] ?? `Stage ${log.sequence_stage}`}
                      </span>
                    </td>
                    <td className="px-4 py-4">
                      {log.status === 'sent' ? (
                        <span className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-100">
                          <CheckCircle2 className="h-3 w-3" /> Sent
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-bold text-amber-700 bg-amber-50 border border-amber-100">
                          <Clock className="h-3 w-3" /> Queued
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
                        <Calendar className="h-3.5 w-3.5 text-slate-400" />
                        {log.next_touch_date
                          ? new Date(log.next_touch_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
                          : '—'}
                      </div>
                    </td>
                    <td className="py-4 pl-4 pr-6 text-right">
                      {log.status !== 'sent' && (
                        <button
                          onClick={() => markSent(log.id)}
                          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-100 transition-all"
                        >
                          <CheckCircle2 className="h-3.5 w-3.5" /> Mark Sent
                        </button>
                      )}
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
