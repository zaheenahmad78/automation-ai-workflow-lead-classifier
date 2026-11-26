'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

export default function Home() {
  const [leads, setLeads] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeads();
  }, []);

  const fetchLeads = async () => {
    try {
      const response = await axios.get(`${API_URL}/leads`);
      setLeads(response.data);
    } catch (error) {
      console.error('Error fetching leads:', error);
    } finally {
      setLoading(false);
    }
  };

  const markContacted = async (id) => {
    try {
      await axios.patch(`${API_URL}/lead/${id}/contact`);
      fetchLeads();
    } catch (error) {
      console.error('Error marking contacted:', error);
    }
  };

  const getClassificationColor = (classification) => {
    switch(classification) {
      case 'Hot': return 'bg-red-100 text-red-800';
      case 'Warm': return 'bg-yellow-100 text-yellow-800';
      case 'Cold': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredLeads = filter === 'all' 
    ? leads 
    : leads.filter(lead => lead.classification === filter);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading leads...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Lead Dashboard</h1>
        
        {/* Filter Dropdown */}
        <div className="mb-6">
          <label className="mr-3 font-semibold">Filter by:</label>
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="px-4 py-2 border rounded-lg bg-white"
          >
            <option value="all">All Leads</option>
            <option value="Hot">Hot 🔥</option>
            <option value="Warm">Warm 🟡</option>
            <option value="Cold">Cold ❄️</option>
          </select>
        </div>

        {/* Leads Table */}
        <div className="bg-white rounded-lg shadow overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phone</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Source</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Message</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Classification</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Suggested Reply</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredLeads.map((lead) => (
                <tr key={lead.id}>
                  <td className="px-6 py-4 whitespace-nowrap">{lead.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{lead.email}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{lead.phone}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs rounded bg-gray-100">{lead.source}</span>
                  </td>
                  <td className="px-6 py-4 max-w-xs">
                    <div className="truncate">{lead.message.substring(0, 60)}...</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getClassificationColor(lead.classification)}`}>
                      {lead.classification}
                    </span>
                  </td>
                  <td className="px-6 py-4 max-w-md">
                    <div className="text-sm text-gray-600">{lead.suggested_reply}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {lead.status !== 'contacted' && (
                      <button
                        onClick={() => markContacted(lead.id)}
                        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
                      >
                        Mark as Contacted
                      </button>
                    )}
                    {lead.status === 'contacted' && (
                      <span className="text-green-600 font-semibold">✓ Contacted</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}