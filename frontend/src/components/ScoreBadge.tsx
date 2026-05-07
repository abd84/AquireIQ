import { cn } from '@/lib/utils';
import { Sparkles, Activity, ShieldAlert, Monitor, Target } from 'lucide-react';

export function ScoreBadge({ score, tier }: { score?: number | null; tier?: string | null }) {
  if (score === undefined || score === null) {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full bg-slate-100/80 backdrop-blur-sm px-3 py-1.5 text-xs font-semibold text-slate-600 ring-1 ring-inset ring-slate-500/20 shadow-sm">
        <Activity className="w-3.5 h-3.5 animate-pulse" />
        Processing...
      </span>
    );
  }

  const getTierColor = (tierStr?: string | null) => {
    switch (tierStr) {
      case 'Tier 1':
        return 'bg-gradient-to-r from-emerald-500/10 to-green-500/10 text-emerald-700 ring-emerald-600/30 shadow-[0_0_15px_rgba(16,185,129,0.3)] animate-pulse-slow';
      case 'Tier 2':
        return 'bg-gradient-to-r from-blue-500/10 to-indigo-500/10 text-blue-700 ring-blue-600/30 shadow-[0_0_15px_rgba(59,130,246,0.3)]';
      case 'Tier 3':
        return 'bg-gradient-to-r from-yellow-500/10 to-amber-500/10 text-yellow-700 ring-yellow-600/30';
      case 'No Fit':
        return 'bg-red-50/50 text-red-700 ring-red-600/20';
      default:
        return 'bg-slate-50/50 text-slate-600 ring-slate-500/20';
    }
  };

  const getTierLabel = (tierStr?: string | null) => {
    switch (tierStr) {
      case 'Tier 1': return { text: 'Hot Target', icon: Target };
      case 'Tier 2': return { text: 'Strong Fit', icon: Sparkles };
      case 'Tier 3': return { text: 'Monitor', icon: Monitor };
      case 'No Fit': return { text: 'Skip', icon: ShieldAlert };
      default: return { text: tierStr ?? 'Unknown', icon: Activity };
    }
  };

  const labelData = getTierLabel(tier);
  const Icon = labelData.icon;

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-bold ring-1 ring-inset backdrop-blur-md transition-all hover:scale-105',
        getTierColor(tier)
      )}
    >
      <Icon className="w-3.5 h-3.5" />
      <span>{score}<span className="opacity-50 text-[10px] ml-[1px]">/100</span></span>
      <span className="hidden sm:inline-block w-px h-3 bg-current opacity-20 mx-0.5"></span>
      <span className="hidden sm:inline-block">{labelData.text}</span>
    </span>
  );
}
