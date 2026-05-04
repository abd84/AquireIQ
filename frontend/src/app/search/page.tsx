import { SearchForm } from "@/components/SearchForm";

export default function SearchPage() {
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
          Sourcing Search
        </h2>
        <p className="mt-1 text-sm leading-6 text-gray-500">
          Discover new M&A targets. The system will use Google Places to identify businesses and automatically push them into the background enrichment pipeline (Scraper, OpenCorporates, Hunter.io, Gemini).
        </p>
      </div>
      <SearchForm />
    </div>
  );
}