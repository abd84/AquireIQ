import Link from "next/link";
import { ArrowRight, Building2, Search, Zap } from "lucide-react";

export default function Home() {
  return (
    <div className="py-12">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className="text-base font-semibold leading-7 text-blue-600">AcquireIQ</h2>
          <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            AI-Powered M&A Deal Sourcing
          </p>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Find, enrich, score, and contact prime acquisition targets. Our automated pipeline evaluates succession readiness and drafts personalized outreach in seconds.
          </p>
        </div>
        
        <div className="mt-16 flex justify-center">
          <Link
            href="/search"
            className="rounded-md bg-blue-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 flex items-center gap-2"
          >
            Start Sourcing <ArrowRight className="h-4 w-4" />
          </Link>
        </div>

        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
          <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-3 lg:gap-y-16">
            <div className="relative pl-16">
              <dt className="text-base font-semibold leading-7 text-gray-900">
                <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600">
                  <Search className="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                Discovery
              </dt>
              <dd className="mt-2 text-base leading-7 text-gray-600">
                Search via Google Places across any US city and state. Pulls name, ratings, domain, and contact basics.
              </dd>
            </div>
            
            <div className="relative pl-16">
              <dt className="text-base font-semibold leading-7 text-gray-900">
                <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600">
                  <Building2 className="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                Enrichment
              </dt>
              <dd className="mt-2 text-base leading-7 text-gray-600">
                Fills in data voids using Web Scraping, OpenCorporates biz details, and Hunter.io executive emails.
              </dd>
            </div>

            <div className="relative pl-16">
              <dt className="text-base font-semibold leading-7 text-gray-900">
                <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600">
                  <Zap className="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                AI Scoring
              </dt>
              <dd className="mt-2 text-base leading-7 text-gray-600">
                Generates a 0-100 Succession Readiness score and custom outreach drafts via Gemini 1.5 Flash.
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  );
}
