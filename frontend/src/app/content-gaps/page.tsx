"use client";

import React, { useState, useEffect } from "react";
import { Layers, AlertCircle, ArrowRight, Sparkles, CheckCircle2 } from "lucide-react";
import { compareCompetitors } from "@/lib/api";
import DataProvenanceBadge from "@/components/common/DataProvenanceBadge";

export default function ContentGapsPage() {
  const [userChan, setUserChan] = useState("@mychannel");
  const [compChan, setCompChan] = useState("@competitor_one");
  const [gaps, setGaps] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchGaps = async () => {
    if (!userChan.trim() || !compChan.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await compareCompetitors(userChan, [compChan]);
      setGaps(res?.content_gaps || []);
    } catch (err: any) {
      setError(err.message || "Failed to compare channels for content gaps.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGaps();
  }, []);

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Content Gap Discovery</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Identify high-traction competitor topics that have zero direct coverage on your channel.
        </p>
      </div>

      <div className="glass-panel p-5">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            fetchGaps();
          }}
          className="grid grid-cols-1 sm:grid-cols-3 gap-3"
        >
          <input
            type="text"
            value={userChan}
            onChange={(e) => setUserChan(e.target.value)}
            placeholder="Your channel handle..."
            className="bg-slate-900/90 border border-slate-700/80 rounded-lg px-3.5 py-2 text-sm text-slate-100"
          />
          <input
            type="text"
            value={compChan}
            onChange={(e) => setCompChan(e.target.value)}
            placeholder="Competitor handle..."
            className="bg-slate-900/90 border border-slate-700/80 rounded-lg px-3.5 py-2 text-sm text-slate-100"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm flex items-center justify-center gap-2"
          >
            <Layers className="w-4 h-4" />
            <span>{loading ? "Scanning Gaps..." : "Find Content Gaps"}</span>
          </button>
        </form>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm">
          {error}
        </div>
      )}

      {loading && (
        <div className="p-8 text-center glass-card rounded-xl border border-slate-800 space-y-2">
          <div className="inline-block w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-xs text-slate-400">Comparing video catalogs and identifying uncovered competitor content gaps...</p>
        </div>
      )}

      {!loading && gaps.length === 0 && !error && (
        <div className="p-8 text-center glass-panel rounded-xl text-slate-400 text-sm">
          No content gaps found between these channels. Try searching another competitor handle.
        </div>
      )}

      <div className="space-y-4">
        {gaps.map((gap, i) => (
          <div key={i} className="glass-card p-5 rounded-xl border border-slate-800 space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span
                  className={`px-2.5 py-0.5 rounded text-xs font-bold ${
                    gap.opportunity_tier === "HIGH OPPORTUNITY"
                      ? "bg-rose-500/15 text-rose-400 border border-rose-500/30"
                      : gap.opportunity_tier === "MEDIUM OPPORTUNITY"
                      ? "bg-amber-500/15 text-amber-400 border border-amber-500/30"
                      : "bg-slate-800 text-slate-300"
                  }`}
                >
                  {gap.opportunity_tier}
                </span>
                <span className="text-xs text-slate-400">Competitor: {gap.competitor_channel}</span>
              </div>
              <span className="text-xs font-semibold text-cyan-400">
                {gap.competitor_views?.toLocaleString()} views ({gap.multiplier}x baseline)
              </span>
            </div>

            <h3 className="text-base font-bold text-white">{gap.topic_title}</h3>
            <p className="text-xs text-slate-300">{gap.explanation}</p>

            <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span className="text-indigo-400 font-medium">{gap.recommended_action}</span>
              <DataProvenanceBadge provenance="Calculated" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
