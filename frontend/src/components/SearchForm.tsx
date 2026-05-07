'use client';

import { useState } from 'react';
import { Search, Sparkles, MapPin, Building2, Hash, ArrowRight } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { apiUrl } from '@/lib/utils';
import { motion } from 'framer-motion';

const INDUSTRY_SUGGESTIONS = [
  'HVAC contractors', 'Dental practices', 'Auto repair shops',
  'Plumbing services', 'Landscaping companies', 'Accounting firms',
  'Physical therapy clinics', 'Veterinary clinics',
];

export function SearchForm() {
  const [query, setQuery] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [maxResults, setMaxResults] = useState(10);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [minAge, setMinAge] = useState(10);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;
    setIsSubmitting(true);
    try {
      const response = await fetch(apiUrl('/api/search'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          city,
          state,
          max_results: maxResults,
          min_business_age: minAge,
        }),
      });
      if (response.ok) router.push('/companies');
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <motion.form
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
      onSubmit={handleSubmit}
      className="w-full max-w-3xl"
    >
      {/* Main search card */}
      <div className="relative bg-white rounded-2xl shadow-xl shadow-slate-200/80 border border-slate-200/60 overflow-hidden">
        {/* Top accent line */}
        <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-blue-500 via-indigo-500 to-violet-500" />

        <div className="p-6 sm:p-8">
          {/* Primary search input */}
          <div className="mb-6">
            <label htmlFor="query" className="block text-xs font-bold uppercase tracking-widest text-slate-500 mb-2">
              Target Industry
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Building2 className="h-5 w-5 text-slate-400" />
              </div>
              <input
                type="text"
                id="query"
                required
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="block w-full rounded-xl border border-slate-200 bg-slate-50 py-3.5 pl-12 pr-4 text-slate-900 text-sm font-medium placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:bg-white transition-all"
                placeholder='e.g. "HVAC contractors" or "dental clinics"'
              />
            </div>

            {/* Quick suggestions */}
            <div className="flex flex-wrap gap-2 mt-3">
              {INDUSTRY_SUGGESTIONS.slice(0, 5).map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setQuery(s)}
                  className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold text-slate-600 bg-slate-100 hover:bg-blue-50 hover:text-blue-700 border border-slate-200 hover:border-blue-200 transition-all"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          {/* Row 2: City + State */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div>
              <label htmlFor="city" className="block text-xs font-bold uppercase tracking-widest text-slate-500 mb-2">
                City <span className="text-slate-400 normal-case font-medium">(optional)</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <MapPin className="h-4 w-4 text-slate-400" />
                </div>
                <input
                  type="text"
                  id="city"
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  className="block w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-9 pr-3 text-slate-900 text-sm font-medium placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:bg-white transition-all"
                  placeholder="Austin"
                />
              </div>
            </div>
            <div>
              <label htmlFor="state" className="block text-xs font-bold uppercase tracking-widest text-slate-500 mb-2">
                State <span className="text-slate-400 normal-case font-medium">(optional)</span>
              </label>
              <input
                type="text"
                id="state"
                value={state}
                onChange={(e) => setState(e.target.value)}
                className="block w-full rounded-xl border border-slate-200 bg-slate-50 py-3 px-4 text-slate-900 text-sm font-medium placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:bg-white transition-all"
                placeholder="TX"
              />
            </div>
          </div>

          {/* Row 3: Max results + Min age */}
          <div className="grid grid-cols-2 gap-4 mb-8">
            <div>
              <label htmlFor="max_results" className="block text-xs font-bold uppercase tracking-widest text-slate-500 mb-2">
                Max Results
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Hash className="h-4 w-4 text-slate-400" />
                </div>
                <input
                  type="number"
                  id="max_results"
                  min={1}
                  max={50}
                  value={maxResults}
                  onChange={(e) => setMaxResults(parseInt(e.target.value))}
                  className="block w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-9 pr-3 text-slate-900 text-sm font-mono font-bold focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:bg-white transition-all"
                />
              </div>
            </div>
            <div>
              <label htmlFor="min_age" className="block text-xs font-bold uppercase tracking-widest text-slate-500 mb-2">
                Min Business Age (yrs)
              </label>
              <input
                type="number"
                id="min_age"
                min={0}
                max={50}
                value={minAge}
                onChange={(e) => setMinAge(parseInt(e.target.value))}
                className="block w-full rounded-xl border border-slate-200 bg-slate-50 py-3 px-4 text-slate-900 text-sm font-mono font-bold focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:bg-white transition-all"
              />
            </div>
          </div>

          {/* Submit */}
          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            type="submit"
            disabled={isSubmitting}
            className="w-full inline-flex items-center justify-center gap-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-3.5 text-sm font-bold text-white shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 hover:from-blue-700 hover:to-indigo-700 disabled:opacity-60 transition-all"
          >
            {isSubmitting ? (
              <>
                <span className="h-4 w-4 rounded-full border-2 border-white/40 border-t-white animate-spin" />
                Running AI pipeline…
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4" />
                Find Targets
                <ArrowRight className="h-4 w-4" />
              </>
            )}
          </motion.button>
        </div>
      </div>

      {/* Pipeline steps below form */}
      {!isSubmitting && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="mt-5 flex items-center justify-center gap-2 flex-wrap"
        >
          {[
            { n: '1', label: 'Business discovery' },
            { n: '2', label: 'Website scraping' },
            { n: '3', label: 'Email lookup' },
            { n: '4', label: 'AI scoring' },
          ].map((step, i) => (
            <div key={step.n} className="flex items-center gap-2">
              <div className="flex items-center gap-1.5 text-xs text-slate-500">
                <span className="flex items-center justify-center w-4 h-4 rounded-full bg-slate-200 text-slate-600 font-bold text-[10px]">
                  {step.n}
                </span>
                {step.label}
              </div>
              {i < 3 && <span className="text-slate-300 text-xs">→</span>}
            </div>
          ))}
        </motion.div>
      )}

      {/* Loading animation */}
      {isSubmitting && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-5 bg-white rounded-xl border border-slate-200 shadow p-5"
        >
          <p className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-4">Pipeline Running</p>
          <div className="space-y-3">
            {[
              'Discovering businesses in your target market…',
              'Scraping company websites for founding data…',
              'Looking up owner contact information…',
              'Generating Succession Readiness scores with AI…',
            ].map((step, i) => (
              <motion.div
                key={step}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.6 }}
                className="flex items-center gap-3"
              >
                <motion.div
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ repeat: Infinity, duration: 1.5, delay: i * 0.6 }}
                  className="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0"
                />
                <span className="text-sm text-slate-600 font-medium">{step}</span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </motion.form>
  );
}
