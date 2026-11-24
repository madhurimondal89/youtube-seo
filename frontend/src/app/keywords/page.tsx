"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import {
  Search,
  Filter,
  Download,
  FileSpreadsheet,
  FileCode,
  FileText,
  HelpCircle,
  TrendingUp,
  Sparkles,
  ChevronDown,
  Info,
} from "lucide-react";
import { researchKeyword } from "@/lib/api";
import { KeywordResearchResponse, KeywordMetricItem } from "@/lib/types";
import { exportKeywordsToCSV, exportToJSON, exportToMarkdown } from "@/lib/export";
import ScoreGauge from "@/components/common/ScoreGauge";
import DataProvenanceBadge from "@/components/common/DataProvenanceBadge";

function KeywordsContent() {
  const searchParams = useSearchParams();
  const initialSeed = searchParams.get("seed") || "youtube automation";

  const [seed, setSeed] = useState(initialSeed);
  const [includeAlphabet, setIncludeAlphabet] = useState(true);
  const [includeModifiers, setIncludeModifiers] = useState(true);
  const [includeQuestions, setIncludeQuestions] = useState(true);
  const [includeComparisons, setIncludeComparisons] = useState(true);
  const [loading, setLoading] = useState(false);
  const [progressText, setProgressText] = useState("");
  const [data, setData] = useState<KeywordResearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedIntent, setSelectedIntent] = useState<string>("ALL");
  const [sortBy, setSortBy] = useState<"opportunity" | "demand" | "competition">("opportunity");
  const [expandedKeyword, setExpandedKeyword] = useState<KeywordMetricItem | null>(null);

  const executeResearch = async (targetSeed: string) => {
    if (!targetSeed.trim()) return;
    setLoading(true);
    setError(null);
    setProgressText("Expanding autocomplete signals...");

    try {
      setTimeout(() => setProgressText("Calculating deterministic competition..."), 600);
      setTimeout(() => setProgressText("Scoring 10-point opportunity index..."), 1200);

      const res = await researchKeyword(
        targetSeed,
        includeAlphabet,
        includeModifiers,
        45,
        includeQuestions,
        includeComparisons
      );
      setData(res);
    } catch (err: any) {
      setError(err.message || "Failed to research keyword.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (initialSeed) {
      executeResearch(initialSeed);
    }
  }, [initialSeed]);

  // Filter & Sort
  const filtered = (data?.keywords || []).filter((item) => {
    if (selectedIntent === "ALL") return true;
    return item.intents.includes(selectedIntent as any);
  });

  const sorted = [...filtered].sort((a, b) => {
    if (sortBy === "opportunity") return b.opportunity_score - a.opportunity_score;
    if (sortBy === "demand") return b.relative_demand - a.relative_demand;
    return a.estimated_competition - b.estimated_competition; // lower competition first
  });

  return (
    <div className="w-full max-w-[1600px] mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Keyword Intelligence</h1>
          <p className="text-xs sm:text-sm text-slate-400">
            Multi-vector suggestion expansion with 10-signal opportunity scoring and no fake search volumes.
          </p>
        </div>

        {data && (
          <div className="flex items-center gap-2">
            <button
              onClick={() => exportKeywordsToCSV(data, `keywords_${data.seed}`)}
              className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs font-medium text-slate-200 flex items-center gap-1.5 transition-colors"
            >
              <FileSpreadsheet className="w-3.5 h-3.5 text-emerald-400" />
              <span>CSV</span>
            </button>
            <button
              onClick={() => exportToJSON(data, `keywords_${data.seed}`)}
              className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs font-medium text-slate-200 flex items-center gap-1.5 transition-colors"
            >
              <FileCode className="w-3.5 h-3.5 text-indigo-400" />
              <span>JSON</span>
            </button>
            <button
              onClick={() => exportToMarkdown(data, `keywords_${data.seed}`)}
              className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs font-medium text-slate-200 flex items-center gap-1.5 transition-colors"
            >
              <FileText className="w-3.5 h-3.5 text-cyan-400" />
              <span>Markdown</span>
            </button>
          </div>
        )}
      </div>

      {/* Search & Expansion Controls */}
      <div className="glass-panel p-5 space-y-4">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            executeResearch(seed);
          }}
          className="flex flex-col sm:flex-row gap-3"
        >
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={seed}
              onChange={(e) => setSeed(e.target.value)}
              placeholder="Enter seed topic (e.g. 'youtube automation', 'python tutorial')..."
              className="w-full bg-slate-900/90 border border-slate-700/80 rounded-lg pl-10 pr-4 py-2.5 text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/30"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium text-sm flex items-center justify-center gap-2 transition-colors shadow-sm"
          >
            <Search className="w-4 h-4" />
            <span>{loading ? "Researching..." : "Research"}</span>
          </button>
        </form>

        <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400 pt-1 border-t border-slate-800/80">
          <label className="flex items-center gap-2 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={includeAlphabet}
              onChange={(e) => setIncludeAlphabet(e.target.checked)}
              className="rounded border-slate-700 bg-slate-900 text-indigo-600 focus:ring-0"
            />
            <span>Alphabet Expansion (A-Z tree)</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={includeModifiers}
              onChange={(e) => setIncludeModifiers(e.target.checked)}
              className="rounded border-slate-700 bg-slate-900 text-indigo-600 focus:ring-0"
            />
            <span>Intent Modifiers (How-to, vs, best, tutorial)</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={includeQuestions}
              onChange={(e) => setIncludeQuestions(e.target.checked)}
              className="rounded border-slate-700 bg-slate-900 text-indigo-600 focus:ring-0"
            />
            <span>Question Tree (Why, Can, What)</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={includeComparisons}
              onChange={(e) => setIncludeComparisons(e.target.checked)}
              className="rounded border-slate-700 bg-slate-900 text-indigo-600 focus:ring-0"
            />
            <span>Comparison Modifiers (vs, or, alternative)</span>
          </label>
        </div>
      </div>

      {/* Loading Progress State */}
      {loading && (
        <div className="glass-card p-6 rounded-xl text-center space-y-3">
          <div className="inline-block w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-sm font-medium text-slate-200">{progressText}</p>
          <span className="text-xs text-slate-500">Querying public YouTube suggest matrix & calculating heuristics...</span>
        </div>
      )}

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/25 text-rose-400 text-sm flex items-center justify-between gap-3">
          <span>{error}</span>
          <button
            onClick={() => executeResearch(seed)}
            className="px-3 py-1 rounded bg-rose-600/30 hover:bg-rose-600/50 text-white text-xs font-semibold transition-colors"
          >
            Retry
          </button>
        </div>
      )}

      {/* Ready to Research / Quick Suggestions */}
      {!data && !loading && !error && (
        <div className="glass-panel p-8 text-center space-y-4">
          <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 mx-auto flex items-center justify-center">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Ready to Discover High-Opportunity Keywords</h3>
            <p className="text-xs text-slate-400 mt-1">
              Type any topic above or click one of these trending creator seeds to expand live autocomplete signals:
            </p>
          </div>
          <div className="flex flex-wrap justify-center gap-2 pt-2">
            {[
              "youtube automation",
              "faceless youtube channel",
              "video editing tutorial",
              "davinci resolve color grading",
              "premiere pro shortcuts",
              "chatgpt for youtube",
              "make money on youtube",
            ].map((suggestSeed) => (
              <button
                key={suggestSeed}
                onClick={() => {
                  setSeed(suggestSeed);
                  executeResearch(suggestSeed);
                }}
                className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-indigo-600/20 border border-slate-700/80 hover:border-indigo-500/50 text-xs text-slate-300 hover:text-white transition-all"
              >
                + {suggestSeed}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Results View */}
      {data && !loading && (
        <div className="space-y-4">
          {/* Summary Overview Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="glass-panel p-4 space-y-1">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Keywords Expanded</span>
              <div className="text-2xl font-bold text-white">{data.total_found}</div>
              <span className="text-[10px] text-indigo-400 font-medium">Multi-vector A-Z discovery</span>
            </div>
            <div className="glass-panel p-4 space-y-1">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Top Opportunity</span>
              <div className="text-2xl font-bold text-emerald-400">
                {data.top_opportunity_keywords[0]?.opportunity_score || 0}/100
              </div>
              <span className="text-[10px] text-slate-400 truncate block">
                {data.top_opportunity_keywords[0]?.keyword || "None"}
              </span>
            </div>
            <div className="glass-panel p-4 space-y-1">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Topic Clusters</span>
              <div className="text-2xl font-bold text-cyan-400">{data.clusters.length}</div>
              <span className="text-[10px] text-slate-400">Pillar &amp; sub-topics mapped</span>
            </div>
            <div className="glass-panel p-4 space-y-1">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Calculated In</span>
              <div className="text-2xl font-bold text-slate-200">{data.execution_time_ms} ms</div>
              <span className="text-[10px] text-emerald-400">Stateless in-memory speed</span>
            </div>
          </div>

          {/* Filter Bar */}
          <div className="flex flex-wrap items-center justify-between gap-3 p-3 rounded-lg bg-slate-950/60 border border-slate-800/80 text-xs">
            <div className="flex items-center gap-2">
              <Filter className="w-3.5 h-3.5 text-slate-400" />
              <span className="text-slate-400">Intent:</span>
              {[
                "ALL",
                "Tutorial",
                "Informational",
                "Commercial",
                "Comparison",
                "Problem/Fix",
              ].map((intent) => (
                <button
                  key={intent}
                  onClick={() => setSelectedIntent(intent)}
                  className={`px-2.5 py-1 rounded-md font-medium transition-colors ${
                    selectedIntent === intent
                      ? "bg-indigo-600 text-white"
                      : "bg-slate-900 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {intent}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-2">
              <span className="text-slate-400">Sort by:</span>
              <select
                value={sortBy}
                onChange={(e: any) => setSortBy(e.target.value)}
                className="bg-slate-900 border border-slate-800 rounded px-2.5 py-1 text-slate-200 focus:outline-none"
              >
                <option value="opportunity">Opportunity Score (Highest)</option>
                <option value="demand">Relative Demand (Highest)</option>
                <option value="competition">Competition (Lowest)</option>
              </select>
            </div>
          </div>

          {/* Keyword Data Table */}
          <div className="glass-panel overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-900/80 text-slate-400 font-semibold border-b border-slate-800 uppercase tracking-wider">
                  <tr>
                    <th className="py-3 px-4">Keyword</th>
                    <th className="py-3 px-4">Opportunity</th>
                    <th className="py-3 px-4">Relative Demand</th>
                    <th className="py-3 px-4">Est. Competition</th>
                    <th className="py-3 px-4">Intents</th>
                    <th className="py-3 px-4">Provenance</th>
                    <th className="py-3 px-4 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {sorted.map((item, idx) => (
                    <tr
                      key={idx}
                      className="hover:bg-slate-900/40 transition-colors cursor-pointer"
                      onClick={() => setExpandedKeyword(item)}
                    >
                      <td className="py-3.5 px-4 font-medium text-slate-100 flex items-center gap-2">
                        <span>{item.keyword}</span>
                        {item.opportunity_score >= 80 && (
                          <span className="px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 text-[10px] font-semibold border border-emerald-500/20">
                            High Opp
                          </span>
                        )}
                      </td>
                      <td className="py-3.5 px-4">
                        <ScoreGauge score={item.opportunity_score} size="sm" />
                      </td>
                      <td className="py-3.5 px-4">
                        <div className="flex items-center gap-2">
                          <div className="w-20 bg-slate-800 h-1.5 rounded-full overflow-hidden">
                            <div
                              className="bg-indigo-500 h-full rounded-full"
                              style={{ width: `${item.relative_demand}%` }}
                            />
                          </div>
                          <span className="text-slate-300 font-medium">{item.relative_demand}/100</span>
                        </div>
                      </td>
                      <td className="py-3.5 px-4">
                        <div className="flex items-center gap-2">
                          <div className="w-20 bg-slate-800 h-1.5 rounded-full overflow-hidden">
                            <div
                              className={`h-full rounded-full ${
                                item.estimated_competition > 65
                                  ? "bg-rose-500"
                                  : item.estimated_competition > 40
                                  ? "bg-amber-500"
                                  : "bg-emerald-500"
                              }`}
                              style={{ width: `${item.estimated_competition}%` }}
                            />
                          </div>
                          <span className="text-slate-300 font-medium">
                            {item.estimated_competition}/100
                          </span>
                        </div>
                      </td>
                      <td className="py-3.5 px-4">
                        <div className="flex flex-wrap gap-1">
                          {item.intents.map((i) => (
                            <span
                              key={i}
                              className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-medium"
                            >
                              {i}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="py-3.5 px-4">
                        <DataProvenanceBadge provenance={item.provenance} />
                      </td>
                      <td className="py-3.5 px-4 text-right">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setExpandedKeyword(item);
                          }}
                          className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium transition-colors"
                        >
                          Details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Transparent Score Breakdown Modal */}
      {expandedKeyword && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-card max-w-xl w-full p-6 rounded-2xl space-y-5 border border-slate-700 max-h-[90vh] overflow-y-auto">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-xs text-indigo-400 font-semibold uppercase tracking-wider">
                  Deterministic Score Analysis
                </span>
                <h3 className="text-xl font-bold text-white mt-0.5">{expandedKeyword.keyword}</h3>
              </div>
              <button
                onClick={() => setExpandedKeyword(null)}
                className="text-slate-400 hover:text-white text-lg font-bold p-1"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4 p-4 rounded-xl bg-slate-900/60 border border-slate-800">
              <ScoreGauge
                score={expandedKeyword.opportunity_score}
                label="Opportunity Score"
                sublabel="Unified 10-signal index"
              />
              <ScoreGauge
                score={expandedKeyword.estimated_competition}
                label="Est. Competition"
                sublabel="Calculated SERP hurdle"
              />
            </div>

            <div className="space-y-3">
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Mathematical Signals</h4>
              <div className="grid grid-cols-2 gap-2 text-xs">
                {Object.entries(expandedKeyword.score_breakdown).map(([k, v]) => (
                  <div key={k} className="p-2.5 rounded-lg bg-slate-900/40 border border-slate-800/80 flex justify-between items-center">
                    <span className="text-slate-400 capitalize">{k.replace(/_/g, " ")}:</span>
                    <span className="font-semibold text-slate-200">{v}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Algorithmic Rationale</h4>
              <ul className="space-y-1.5">
                {expandedKeyword.reasons.map((r, i) => (
                  <li key={i} className="text-xs text-slate-300 flex items-start gap-2">
                    <span className="text-emerald-400 font-bold">•</span>
                    <span>{r}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="pt-2 border-t border-slate-800 flex justify-end">
              <button
                onClick={() => setExpandedKeyword(null)}
                className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function KeywordsPage() {
  return (
    <Suspense fallback={<div className="text-slate-400 p-8">Loading keywords...</div>}>
      <KeywordsContent />
    </Suspense>
  );
}
