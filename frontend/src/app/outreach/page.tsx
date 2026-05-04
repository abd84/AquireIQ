'use client';

import { useEffect, useState } from 'react';
import { Mail, Calendar, CheckCircle2 } from 'lucide-react';
import Link from 'next/link';

type OutreachLog = {
  id: string;
  company_id: string;
  contact_email: string;
  sequence_stage: number;
  status: string;
  next_touch_date: string;
};

export default function OutreachQueuePage() {
  const [logs, setLogs] = useState<OutreachLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/outreach');
        if (res.ok) {
          const data = await res.json();
          setLogs(data);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const markSent = async (id: string) => {
    try {
      await fetch(`http://localhost:8000/api/outreach/${id}/mark-sent`, { method: 'PATCH' });
      setLogs(logs.map(l => l.id === id ? { ...l, status: 'sent' } : l));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-base font-semibold leading-6 text-gray-900">Outreach Queue</h1>
          <p className="mt-2 text-sm text-gray-700">
            A list of all contacts targeted for sequencing. Manually mark them exported/sent if using an external mailer to track status.
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
                      Contact
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Company Match
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Status
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                      Next Touch
                    </th>
                    <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                      <span className="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white">
                  {loading ? (
                    <tr>
                      <td colSpan={5} className="text-center py-10 text-gray-500">Loading queue...</td>
                    </tr>
                  ) : logs.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="text-center py-10 text-gray-500">Queue is empty.</td>
                    </tr>
                  ) : (
                    logs.map((log) => (
                      <tr key={log.id}>
                        <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm sm:pl-6">
                          <div className="flex items-center">
                            <Mail className="h-5 w-5 text-gray-400 mr-3" />
                            <span className="font-medium text-gray-900">{log.contact_email || 'No email found'}</span>
                          </div>
                        </td>
                        <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                          <Link href={`/companies/${log.company_id}`} className="text-blue-600 hover:underline">
                            View Company
                          </Link>
                        </td>
                        <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                           <span className={`inline-flex items-center gap-1.5 rounded-full px-2 py-1 text-xs font-medium ${log.status === 'sent' ? 'text-green-700 bg-green-50' : 'text-yellow-800 bg-yellow-50'}`}>
                              {log.status === 'sent' ? <CheckCircle2 className="h-3 w-3" /> : null}
                              {log.status} (Stage {log.sequence_stage})
                            </span>
                        </td>
                        <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 flex items-center gap-2">
                          <Calendar className="h-4 w-4" />
                          {log.next_touch_date ? new Date(log.next_touch_date).toLocaleDateString() : 'N/A'}
                        </td>
                        <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                          {log.status !== 'sent' && (
                             <button
                               onClick={() => markSent(log.id)}
                               className="text-blue-600 hover:text-blue-900"
                             >
                               Mark Sent
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