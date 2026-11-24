"use client";

import React, { useState } from "react";
import { UserCheck, Sparkles, TrendingUp, CheckCircle2, ArrowRight } from "lucide-react";
import { auditChannel } from "@/lib/api";
import { ChannelAuditResult } from "@/lib/types";
import ScoreGauge from "@/components/common/ScoreGauge";
import DataProvenanceBadge from "@/components/common/DataProvenanceBadge";

export default function ChannelAuditPage() {
  const [handle, setHandle] = useState("@creatoracademy");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ChannelAuditResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAudit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!handle.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await auditChannel(handle);
      setResult(res);
    } catch (err: any) {
      setError(err.message || "Failed to audit channel.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Channel SEO Audit</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Macro channel audit evaluating topic consistency, title packaging quality, and upload cadence.
        </p>
      </div>

      {/* Input */}
      <div className="glass-panel p-5">
        <form onSubmit={handleAudit} className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={handle}
            onChange={(e) => setHandle(e.target.value)}
            placeholder="Enter channel handle (e.g. '@mkbhd', 'UC...') or custom URL..."
            className="flex-1 bg-slate-900/90 border border-slate-700/80 rounded-lg px-4 py-2.5 text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:border-indigo-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm flex items-center justify-center gap-2"
          >
            <UserCheck className="w-4 h-4" />
            <span>{loading ? "Auditing..." : "Audit Channel"}</span>
          </button>
        </form>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm">
          {error}
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="space-y-6">
          {/* Header */}
          <div className="glass-card p-6 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-6 border border-slate-800">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Channel Audit</span>
                <DataProvenanceBadge provenance={result.provenance} />
              </div>
              <h2 className="text-2xl font-bold text-white">{result.channel_title}</h2>
              <span className="text-xs text-indigo-400 font-mono">ID: {result.channel_id}</span>
            </div>
            <ScoreGauge score={result.overall_health_score} size="lg" label="Channel Health" sublabel="Macro SEO Score" />
          </div>

          {/* Pillars Scores */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="glass-card p-5 rounded-xl flex items-center justify-between">
              <div className="space-y-1">
                <span className="text-xs text-slate-400">Topic Consistency</span>
                <div className="text-xl font-bold text-white">{result.topic_consistency_score}/100</div>
              </div>
              <ScoreGauge score={result.topic_consistency_score} size="sm" />
            </div>

            <div className="glass-card p-5 rounded-xl flex items-center justify-between">
              <div className="space-y-1">
                <span className="text-xs text-slate-400">Title Packaging Quality</span>
                <div className="text-xl font-bold text-white">{result.title_quality_score}/100</div>
              </div>
              <ScoreGauge score={result.title_quality_score} size="sm" />
            </div>

            <div className="glass-card p-5 rounded-xl flex items-center justify-between">
              <div className="space-y-1">
                <span className="text-xs text-slate-400">Outlier Ratio</span>
                <div className="text-xl font-bold text-cyan-400">{Math.round(result.outlier_ratio * 100)}%</div>
                <span className="text-[11px] text-slate-400">Videos exceeding 2.5x median</span>
              </div>
              <div className="w-10 h-10 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
                <TrendingUp className="w-5 h-5" />
              </div>
            </div>
          </div>

          {/* Recommendations & Next Best Topics */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-panel p-6 rounded-xl space-y-3">
              <h3 className="text-sm font-bold text-white">Strategic Channel Recommendations</h3>
              <ul className="space-y-2">
                {result.recommendations.map((r, i) => (
                  <li key={i} className="text-xs text-slate-300 flex items-start gap-2">
                    <span className="text-indigo-400 font-bold">•</span>
                    <span>{r}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="glass-panel p-6 rounded-xl space-y-3">
              <h3 className="text-sm font-bold text-white">Recommended Next Video Topics</h3>
              <ul className="space-y-2">
                {result.next_best_video_topics.map((t, i) => (
                  <li key={i} className="text-xs text-slate-300 flex items-start gap-2">
                    <span className="text-cyan-400 font-bold">•</span>
                    <span>{t}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
