'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard,
  Users,
  Search,
  Mail,
  Menu,
  X,
  TrendingUp,
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Sourcing Search', href: '/search', icon: Search },
  { name: 'Company Leads', href: '/companies', icon: Users },
  { name: 'Outreach Queue', href: '/outreach', icon: Mail },
];

export function SidebarLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-slate-50">

      {/* ── Background decoration ───────────────────────────── */}
      <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
        {/* Dot grid */}
        <div
          className="absolute inset-0 opacity-[0.35]"
          style={{
            backgroundImage:
              'radial-gradient(circle, #94a3b8 1px, transparent 1px)',
            backgroundSize: '28px 28px',
          }}
        />
        {/* Gradient blobs */}
        <div className="absolute -top-40 -right-40 w-[700px] h-[700px] rounded-full bg-gradient-to-br from-blue-400/20 to-indigo-500/20 blur-[100px]" />
        <div className="absolute top-1/2 -left-40 w-[500px] h-[500px] rounded-full bg-gradient-to-tr from-violet-400/15 to-sky-400/15 blur-[80px]" />
        <div className="absolute -bottom-20 right-1/3 w-[400px] h-[400px] rounded-full bg-gradient-to-t from-emerald-400/10 to-teal-400/10 blur-[80px]" />
        {/* Fade from bottom so grid doesn't look too busy */}
        <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-slate-50 to-transparent" />
      </div>

      {/* ── Mobile overlay ──────────────────────────────────── */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            key="overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-sm lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* ── Mobile sidebar drawer ───────────────────────────── */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            key="drawer"
            initial={{ x: '-100%' }}
            animate={{ x: 0 }}
            exit={{ x: '-100%' }}
            transition={{ type: 'spring', stiffness: 320, damping: 32 }}
            className="fixed inset-y-0 left-0 z-50 w-72 lg:hidden"
          >
            <SidebarContent pathname={pathname} onClose={() => setSidebarOpen(false)} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Mobile top bar ──────────────────────────────────── */}
      <div className="sticky top-0 z-30 flex items-center gap-4 px-4 py-3 bg-white/70 backdrop-blur-xl border-b border-slate-200/60 shadow-sm lg:hidden">
        <button
          onClick={() => setSidebarOpen(true)}
          className="p-2 rounded-xl bg-white shadow-sm border border-slate-200 text-slate-600 hover:text-blue-600 transition-colors"
        >
          <Menu className="h-5 w-5" />
        </button>
        <div className="flex items-center gap-2">
          <div className="flex items-center justify-center w-7 h-7 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-600 shadow">
            <TrendingUp className="h-4 w-4 text-white" strokeWidth={2.5} />
          </div>
          <span className="text-base font-black tracking-tight text-slate-900">AcquireIQ</span>
        </div>
      </div>

      {/* ── Desktop sidebar ─────────────────────────────────── */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:left-0 lg:z-40 lg:w-64 lg:flex lg:flex-col">
        <SidebarContent pathname={pathname} />
      </div>

      {/* ── Main content ────────────────────────────────────── */}
      <div className="lg:pl-64">
        <main className="min-h-screen">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-10 py-8 lg:py-10">
            <AnimatePresence mode="popLayout">
              <motion.div
                key={pathname}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.3, ease: 'easeOut' }}
              >
                {children}
              </motion.div>
            </AnimatePresence>
          </div>
        </main>
      </div>
    </div>
  );
}

function SidebarContent({
  pathname,
  onClose,
}: {
  pathname: string;
  onClose?: () => void;
}) {
  return (
    <div className="flex h-full flex-col bg-white/80 backdrop-blur-2xl border-r border-slate-200/70 shadow-xl">
      {/* Logo */}
      <div className="flex items-center justify-between px-5 py-5 border-b border-slate-100">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 shadow-md shadow-blue-500/30">
            <TrendingUp className="h-5 w-5 text-white" strokeWidth={2.5} />
          </div>
          <div>
            <p className="text-lg font-black tracking-tight text-slate-900">AcquireIQ</p>
            <p className="text-[10px] font-semibold text-slate-400 uppercase tracking-widest -mt-0.5">M&amp;A Intelligence</p>
          </div>
        </div>
        {onClose && (
          <button onClick={onClose} className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors">
            <X className="h-4 w-4" />
          </button>
        )}
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <p className="px-3 mb-2 text-[10px] font-bold uppercase tracking-widest text-slate-400">Navigation</p>
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              onClick={onClose}
              className={cn(
                'relative flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200',
                isActive
                  ? 'text-blue-700 bg-blue-50 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
              )}
            >
              {isActive && (
                <motion.div
                  layoutId="activeNav"
                  className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-r-full"
                  transition={{ type: 'spring', stiffness: 380, damping: 30 }}
                />
              )}
              <item.icon
                className={cn(
                  'h-4.5 w-4.5 shrink-0 transition-colors',
                  isActive ? 'text-blue-600' : 'text-slate-400 group-hover:text-slate-600'
                )}
                aria-hidden="true"
              />
              {item.name}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="px-4 py-4 border-t border-slate-100">
        <div className="rounded-xl bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100 p-3">
          <p className="text-xs font-bold text-blue-800">AI Pipeline Active</p>
          <p className="text-[11px] text-blue-600 mt-0.5">Discovery · Enrichment · Scoring</p>
        </div>
      </div>
    </div>
  );
}
