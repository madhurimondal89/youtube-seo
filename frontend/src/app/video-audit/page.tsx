"use client";

import React, { useState } from "react";
import { Video, CheckCircle2, AlertTriangle, XCircle, ArrowRight, Sparkles, Wrench, Subtitles, Image as ImageIcon } from "lucide-react";
import { auditVideo } from "@/lib/api";
import { VideoAuditResult } from "@/lib/types";
import ScoreGauge from "@/components/common/ScoreGauge";
import DataProvenanceBadge from "@/components/common/DataProvenanceBadge";
import SerpThumbnailPreview from "@/components/common/SerpThumbnailPreview";

export default function VideoAuditPage() {
  const [url, setUrl] = useState("");
  const [title, setTitle] = useState("How to Rank YouTube Videos Fast in 2026: Complete SEO Guide");
  const [desc, setDesc] = useState(
    "In this comprehensive video we explore how to rank youtube videos fast with practical keyword optimization and title formulas.\n\n00:00 - Introduction\n02:30 - Autocomplete Research\n06:00 - Metadata Setup\n\nSubscribe for weekly creator tutorials! #YouTubeSEO #VideoMarketing"
  );
  const [tags, setTags] = useState("youtube seo, rank youtube videos fast, youtube keyword research, video seo 2026");
  const [targetKw, setTargetKw] = useState("rank youtube videos fast");
  const [hasCaptions, setHasCaptions] = useState(false);
  const [thumbUrl, setThumbUrl] = useState("");
  const [mode, setMode] = useState<"manual" | "url">("manual");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<VideoAuditResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const runAudit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const tagList = tags.split(",").map((t) => t.trim()).filter(Boolean);
      const res = await auditVideo(
        mode === "url" ? url : undefined,
        mode === "manual" ? title : undefined,
        mode === "manual" ? desc : undefined,
        tagList,
        targetKw,
        hasCaptions
      );
      setResult(res);
    } catch (err: any) {
      setError(err.message || "Failed to audit video.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">18-Point Video SEO Audit</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Deterministic 0-100 score breakdown across Title, Description, Tags, Keyword Alignment, and Search Intent.
        </p>
      </div>

      {/* Input Selector */}
      <div className="glass-panel p-6 space-y-4">
        <div className="flex gap-4 border-b border-slate-800 pb-3 text-sm">
          <button
            onClick={() => setMode("manual")}
            className={`font-semibold transition-colors ${
              mode === "manual" ? "text-indigo-400 border-b-2 border-indigo-500 pb-1" : "text-slate-400"
            }`}
          >
            Manual Metadata Input
          </button>
          <button
            onClick={() => setMode("url")}
            className={`font-semibold transition-colors ${
              mode === "url" ? "text-indigo-400 border-b-2 border-indigo-500 pb-1" : "text-slate-400"
            }`}
          >
            Public YouTube Video URL
          </button>
        </div>

        <form onSubmit={runAudit} className="space-y-4">
          {mode === "url" ? (
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">YouTube Video URL</label>
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://www.youtube.com/watch?v=..."
                className="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3.5 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              />
            </div>
          ) : (
            <>
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Target Focus Keyword</label>
                <input
                  type="text"
                  value={targetKw}
                  onChange={(e) => setTargetKw(e.target.value)}
                  placeholder="e.g. 'rank youtube videos fast'"
                  className="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3.5 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Video Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Enter video title..."
                  className="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3.5 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Video Description</label>
                <textarea
                  rows={4}
                  value={desc}
                  onChange={(e) => setDesc(e.target.value)}
                  placeholder="Paste video description..."
                  className="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3.5 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Video Tags (comma separated)</label>
                <input
                  type="text"
                  value={tags}
                  onChange={(e) => setTags(e.target.value)}
                  placeholder="tag 1, tag 2, tag 3..."
                  className="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3.5 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">Custom Thumbnail URL (optional)</label>
                  <input
                    type="text"
                    value={thumbUrl}
                    onChange={(e) => setThumbUrl(e.target.value)}
                    placeholder="https://..."
                    className="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3.5 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <div className="flex items-center gap-3 pt-5">
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={hasCaptions}
                      onChange={(e) => setHasCaptions(e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-10 h-5 bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-indigo-600"></div>
                  </label>
                  <span className="text-xs font-medium text-slate-300 flex items-center gap-1.5">
                    <Subtitles className="w-3.5 h-3.5 text-indigo-400" />
                    <span>Video Has Closed Captions / Subtitles (CC)</span>
                  </span>
                </div>
              </div>
            </>
          )}

          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm flex items-center gap-2 transition-colors"
          >
            <Video className="w-4 h-4" />
            <span>{loading ? "Auditing..." : "Calculate SEO Score"}</span>
          </button>
        </form>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm">
          {error}
        </div>
      )}

      {/* Audit Output */}
      {result && (
        <div className="space-y-6">
          {/* Header Score Card */}
          <div className="glass-card p-6 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-6 border border-slate-800">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Overall SEO Health</span>
                <DataProvenanceBadge provenance={result.provenance} />
              </div>
              <h2 className="text-2xl font-bold text-white">{result.title}</h2>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-bold border border-emerald-500/20">
                <span>Verdict: {result.verdict}</span>
              </div>
            </div>
            <ScoreGauge score={result.overall_score} size="lg" label="Total SEO Score" sublabel="Out of 100 points" />
          </div>

          {/* Interactive SERP & Thumbnail Preview */}
          <SerpThumbnailPreview
            title={result.title}
            description={desc}
            thumbnailUrl={thumbUrl}
            hasChapters={desc.includes("00:00") || desc.includes("0:00")}
            hasCaptions={hasCaptions}
            onThumbnailChange={(url) => setThumbUrl(url)}
          />

          {/* Action Plan */}
          {result.action_plan.length > 0 && (
            <div className="p-5 rounded-xl bg-indigo-950/30 border border-indigo-500/30 space-y-3">
              <h3 className="text-sm font-bold text-indigo-300 flex items-center gap-2">
                <Wrench className="w-4 h-4" /> Prioritized Action Items
              </h3>
              <ul className="space-y-1.5">
                {result.action_plan.map((item, idx) => (
                  <li key={idx} className="text-xs text-slate-200 flex items-start gap-2">
                    <span className="text-indigo-400 font-bold">•</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 7-Category Checklist Breakdown */}
          <div className="space-y-4">
            <h3 className="text-lg font-bold text-white">Category Breakdown</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {result.categories.map((cat, i) => (
                <div key={i} className="glass-panel p-5 rounded-xl space-y-3">
                  <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                    <span className="font-bold text-sm text-slate-200">{cat.category_name}</span>
                    <span className="text-xs font-semibold text-emerald-400">
                      {cat.earned_score} / {cat.max_score} pts ({cat.percentage}%)
                    </span>
                  </div>

                  <div className="space-y-2">
                    {cat.items.map((item) => (
                      <div key={item.id} className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800/80 space-y-1">
                        <div className="flex items-center justify-between text-xs">
                          <span className="font-medium text-slate-200 flex items-center gap-1.5">
                            {item.passed ? (
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                            ) : item.severity === "warning" ? (
                              <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                            ) : (
                              <XCircle className="w-3.5 h-3.5 text-rose-400" />
                            )}
                            {item.title}
                          </span>
                          <span className="text-slate-400 font-mono">
                            {item.score_earned}/{item.max_score}
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-400 pl-5">{item.feedback}</p>
                        {item.actionable_fix && (
                          <p className="text-[11px] text-indigo-300 pl-5 font-medium">
                            Fix: {item.actionable_fix}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
