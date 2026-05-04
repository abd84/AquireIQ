'use client';

import { useEffect, useState } from 'react';
import { ScoreBadge } from '@/components/ScoreBadge';
import { Building2, Mail, ExternalLink, MapPin, Phone, Users, Briefcase, ChevronLeft } from 'lucide-react';
import Link from 'next/link';

export default function CompanyDetailPage({ params }: { params: { id: string } }) {
  const [company, setCompany] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCompany = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/companies/${params.id}`);
        if (res.ok) {
          const data = await res.json();
          setCompany(data);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchCompany();
  }, [params.id]);

  if (loading) return <div className="py-10 text-center">Loading details...</div>;
  if (!company) return <div className="py-10 text-center">Company not found.</div>;

  return (
    <div>
      <div className="mb-6">
        <Link href="/companies" className="text-sm font-semibold leading-6 text-blue-600 flex items-center gap-1 hover:text-blue-500">
          <ChevronLeft className="h-4 w-4" /> Back to Leads
        </Link>
      </div>

      <div className="md:flex md:items-center md:justify-between md:space-x-5 border-b border-gray-200 pb-5 mb-8">
        <div className="flex items-start space-x-5">
          <div className="flex-shrink-0">
             <div className="h-16 w-16 flex items-center justify-center bg-gray-100 rounded-lg">
                <Building2 className="h-8 w-8 text-gray-500" />
             </div>
          </div>
          <div className="pt-1.5">
            <h1 className="text-2xl font-bold text-gray-900">{company.name}</h1>
            <p className="text-sm font-medium text-gray-500 flex items-center gap-2 mt-1">
               {company.industry_description || 'Unknown Industry'}
               {company.domain && (
                 <a href={`https://${company.domain}`} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline flex items-center gap-1">
                   {company.domain} <ExternalLink className="h-3 w-3" />
                 </a>
               )}
            </p>
          </div>
        </div>
        <div className="mt-6 flex flex-col-reverse justify-stretch space-y-4 space-y-reverse sm:flex-row-reverse sm:justify-end sm:space-x-3 sm:space-y-0 sm:space-x-reverse md:mt-0 md:flex-row md:space-x-3">
          <ScoreBadge score={company.acquisition_score} tier={company.score_tier} />
          {company.owner_email && (
            <button
              type="button"
              className="inline-flex items-center justify-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
            >
              <Mail className="-ml-0.5 mr-1.5 h-4 w-4" aria-hidden="true" />
              Queue Outreach
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-x-8 gap-y-8 lg:grid-cols-3">
        <div className="lg:col-span-2">
          {/* AI Explanation */}
          <section aria-labelledby="ai-explanation-title">
            <div className="bg-white shadow sm:rounded-lg mb-8">
              <div className="px-4 py-5 sm:px-6">
                <h2 id="ai-explanation-title" className="text-lg font-medium leading-6 text-gray-900">
                  AI Succession Analysis
                </h2>
              </div>
              <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                <p className="text-gray-700 whitespace-pre-wrap">{company.score_explanation || "No AI explanation available yet. Ensure enrichment pipeline completed."}</p>
              </div>
            </div>
          </section>

          {/* AI Draft Email */}
          {company.outreach_body && (
            <section aria-labelledby="ai-email-title">
              <div className="bg-white shadow sm:rounded-lg">
                <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
                  <h2 id="ai-email-title" className="text-lg font-medium leading-6 text-gray-900">
                    Draft Outreach Email
                  </h2>
                </div>
                <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                  <div className="mb-4">
                    <span className="font-semibold text-sm text-gray-700">Subject: </span>
                    <span className="text-sm text-gray-900">{company.outreach_subject}</span>
                  </div>
                  <div className="bg-gray-50 rounded-md p-4 text-sm text-gray-700 whitespace-pre-wrap border border-gray-200">
                    {company.outreach_body}
                  </div>
                </div>
              </div>
            </section>
          )}
        </div>

        <div className="space-y-8 lg:col-span-1">
          {/* Overview Info */}
          <section aria-labelledby="overview-title">
            <div className="bg-white shadow sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                <h2 id="overview-title" className="text-lg font-medium leading-6 text-gray-900">
                  Business Overview
                </h2>
              </div>
              <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                <dl className="grid grid-cols-1 gap-x-4 gap-y-6">
                   <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500 flex items-center gap-2"><MapPin className="h-4 w-4"/> Location</dt>
                    <dd className="mt-1 text-sm text-gray-900">{company.hq_city && company.hq_state ? `${company.hq_city}, ${company.hq_state}` : 'Unknown'}</dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500 flex items-center gap-2"><Phone className="h-4 w-4"/> Phone</dt>
                    <dd className="mt-1 text-sm text-gray-900">{company.phone || 'Unknown'}</dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500 flex items-center gap-2"><Briefcase className="h-4 w-4"/> Founded</dt>
                    <dd className="mt-1 text-sm text-gray-900">{company.founded_year || 'Unknown'}</dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500 flex items-center gap-2"><Users className="h-4 w-4"/> Employees</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                       {company.employee_count_low ? `${company.employee_count_low} - ${company.employee_count_high}` : 'Unknown'}
                    </dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Google Rating</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {company.google_rating ? `${company.google_rating} (${company.google_review_count} reviews)` : 'Unknown'}
                    </dd>
                  </div>
                </dl>
              </div>
            </div>
          </section>

          {/* Owner Info */}
          <section aria-labelledby="owner-title">
            <div className="bg-white shadow sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                <h2 id="owner-title" className="text-lg font-medium leading-6 text-gray-900">
                  Key Contact
                </h2>
              </div>
              <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
                <dl className="grid grid-cols-1 gap-x-4 gap-y-6">
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Name</dt>
                    <dd className="mt-1 text-sm text-gray-900">{company.owner_name || 'Not Identified'}</dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Email</dt>
                    <dd className="mt-1 text-sm text-gray-900">{company.owner_email || 'Not Extracted'}</dd>
                  </div>
                </dl>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}