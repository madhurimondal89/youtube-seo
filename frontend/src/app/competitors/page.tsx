"use client";

import React, { useState } from "react";
import { Users, Layers, TrendingUp, ArrowRight } from "lucide-react";
import { compareCompetitors } from "@/lib/api";
import { CompetitorComparisonResult } from "@/lib/types";
import DataProvenanceBadge from "@/components/common/DataProvenanceBadge";

export default function CompetitorsPage() {
  const [userChan, setUserChan] = useState("@mychannel");
  const [compChan1, setCompChan1] = useState("@competitor_one");
  const [compChan2, setCompChan2] = useState("@competitor_two");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CompetitorComparisonResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleCompare = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const comps = [compChan1, compChan2].filter((c) => c.trim().length > 0);
      const res = await compareCompetitors(userChan, comps);
      setResult(res);
    } catch (err: any) {
      setError(err.message || "Failed to compare competitors.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Competitor Intelligence</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Compare observable public performance baselines, median views, upload velocities, and content gaps.
        </p>
      </div>

      {/* Input */}
      <div className="glass-panel p-5">
        <form onSubmit={handleCompare} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Your Channel</label>
              <input
                type="text"
                value={userChan}
                onChange={(e) => setUserChan(e.target.value)}
                placeholder="@yourchannel"
                className="w-full bg-slate-900/90 border border-slate-700/80 rounded-lg px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Competitor 1</label>
              <input
                type="text"
                value={compChan1}
                onChange={(e) => setCompChan1(e.target.value)}
                placeholder="@competitor_one"
                className="w-full bg-slate-900/90 border border-slate-700/80 rounded-lg px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Competitor 2</label>
              <input
                type="text"
                value={compChan2}
                onChange={(e) => setCompChan2(e.target.value)}
                placeholder="@competitor_two"
                className="w-full bg-slate-900/90 border border-slate-700/80 rounded-lg px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm flex items-center gap-2"
          >
            <Users className="w-4 h-4" />
            <span>{loading ? "Analyzing..." : "Compare Competitors"}</span>
          </button>
        </form>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm">
          {error}
        </div>
      )}

      {/* Comparison Grid */}
      {result && (
        <div className="space-y-6">
          <div className="glass-panel overflow-hidden">
            <div className="p-4 border-b border-slate-800 flex items-center justify-between">
              <span className="font-bold text-sm text-white">Channel Performance Benchmark</span>
              <DataProvenanceBadge provenance={result.provenance} />
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-900/80 text-slate-400 font-semibold border-b border-slate-800 uppercase tracking-wider">
                  <tr>
                    <th className="py-3 px-4">Channel</th>
                    <th className="py-3 px-4">Median Views</th>
                    <th className="py-3 px-4">MAD (Dispersion)</th>
                    <th className="py-3 px-4">Upload Cadence</th>
                    <th className="py-3 px-4">Avg Duration</th>
                    <th className="py-3 px-4">Outliers Detected</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {Object.entries(result.metrics_by_channel).map(([chanTitle, metrics]) => (
                    <tr key={chanTitle} className="hover:bg-slate-900/40">
                      <td className="py-3.5 px-4 font-bold text-slate-100">{chanTitle}</td>
                      <td className="py-3.5 px-4 font-semibold text-indigo-400">
                        {metrics.median_views.toLocaleString()} views
                      </td>
                      <td className="py-3.5 px-4 text-slate-300">±{metrics.mad_views.toLocaleString()}</td>
                      <td className="py-3.5 px-4 text-slate-300">{metrics.upload_frequency_per_month} / mo</td>
                      <td className="py-3.5 px-4 text-slate-300">
                        {Math.floor(metrics.average_duration_seconds / 60)}m {metrics.average_duration_seconds % 60}s
                      </td>
                      <td className="py-3.5 px-4">
                        <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold border border-emerald-500/20">
                          {metrics.outlier_count} videos
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
