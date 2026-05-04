import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function ScoreBadge({ score, tier }: { score?: number | null; tier?: string | null }) {
  if (score === undefined || score === null) {
    return <span className="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10">Pending</span>;
  }

  const getTierColor = (tierStr?: string | null) => {
    switch (tierStr) {
      case 'Tier 1 (Prime Target)':
        return 'bg-green-50 text-green-700 ring-green-600/20';
      case 'Tier 2 (Good Target)':
        return 'bg-blue-50 text-blue-700 ring-blue-600/20';
      case 'Tier 3 (Average Target)':
        return 'bg-yellow-50 text-yellow-800 ring-yellow-600/20';
      case 'Tier 4 (Low Priority)':
        return 'bg-red-50 text-red-700 ring-red-600/10';
      default:
        return 'bg-gray-50 text-gray-600 ring-gray-500/10';
    }
  };

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset",
        getTierColor(tier)
      )}
    >
      {score} / 100 - {tier?.split(' ')[0] || 'Unknown'}
    </span>
  );
}