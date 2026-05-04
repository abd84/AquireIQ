'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { ScoreBadge } from '@/components/ScoreBadge';
import { Building2, Mail, ExternalLink, Activity } from 'lucide-react';

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

export default function CompaniesPage() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);

  // Poll for updates if there are enriching companies
  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/companies');
        if (res.ok) {
          const data = await res.json();
          setCompanies(data);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchCompanies();
    
    // Poll every 5s to catch enrichment updates
    const interval = setInterval(() => {
      fetchCompanies();
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);

  const formatRevenue = (low?: number, high?: number) => {
    if (!low && !high) return 'Unknown';
    const l = low ? `$${(low / 1000000).toFixed(1)}M` : '';
    const h = high ? `$${(high / 1000000).toFixed(1)}M` : '';
    if (l && h) return `${l} - ${h}`;
    return l || h;
  };

  return (
    <div>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-base font-semibold leading-6 text-gray-900">Company Leads</h1>
          <p className="mt-2 text-sm text-gray-700">
            A list of all sourced companies, their estimated revenue, and Succession Readiness Score.
          </p>
        </div>
      </div>
      <div className="mt-8 flow-root">
        <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
              <table className="min-w-full divide-y divide-gray-300">
                <thead className="bg-gray-50">
                  <tr>
                    <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                      Company
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Location
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Est. Revenue
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Score
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Status
                    </th>
                    <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                      <span className="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white">
                  {loading ? (
                    <tr>
                      <td colSpan={6} className="text-center py-10 text-gray-500">Loading companies...</td>
                    </tr>
                  ) : companies.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="text-center py-10 text-gray-500">No leads found. Start a search first.</td>
                    </tr>
                  ) : (
                    companies.map((company) => (
                      <tr key={company.id}>
                        <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm sm:pl-6">
                          <div className="flex items-center">
                            <div className="h-10 w-10 flex-shrink-0 flex items-center justify-center bg-gray-100 rounded-md">
                              <Building2 className="h-5 w-5 text-gray-500" />
                            </div>
                            <div className="ml-4">
                              <div className="font-medium text-gray-900 flex items-center gap-2">
                                <Link href={`/companies/${company.id}`} className="hover:text-blue-600 hover:underline">
                                  {company.name}
                                </Link>
                                {company.domain && (
                                  <a href={`https://${company.domain}`} target="_blank" rel="noreferrer">
                                    <ExternalLink className="h-3 w-3 text-gray-400 hover:text-blue-500" />
                                  </a>
                                )}
                              </div>
                              <div className="text-gray-500">
                                {company.owner_name ? `Owner: ${company.owner_name}` : company.industry_description || 'Unknown Industry'}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                          {company.hq_city && company.hq_state ? `${company.hq_city}, ${company.hq_state}` : 'N/A'}
                        </td>
                        <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                          {formatRevenue(company.revenue_estimate_low, company.revenue_estimate_high)}
                        </td>
                        <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                          <ScoreBadge score={company.acquisition_score} tier={company.score_tier} />
                        </td>
                        <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                          {company.enrichment_status === 'enriching' ? (
                            <span className="inline-flex items-center gap-1.5 rounded-full px-2 py-1 text-xs font-medium text-gray-600 bg-gray-100">
                              <Activity className="h-3 w-3 animate-spin"/> Enriching
                            </span>
                          ) : company.enrichment_status === 'completed' ? (
                            <span className="inline-flex items-center gap-1.5 rounded-full px-2 py-1 text-xs font-medium text-green-700 bg-green-50">
                              Ready
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1.5 rounded-full px-2 py-1 text-xs font-medium text-yellow-800 bg-yellow-50">
                              {company.enrichment_status}
                            </span>
                          )}
                        </td>
                        <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                           <Link href={`/companies/${company.id}`} className="text-blue-600 hover:text-blue-900 mr-4">
                            View<span className="sr-only">, {company.name}</span>
                          </Link>
                          {company.owner_email && (
                            <button className="text-gray-400 hover:text-gray-600">
                              <Mail className="h-4 w-4" />
                            </button>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}