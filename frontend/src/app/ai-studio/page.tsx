"use client";

import React, { useState } from "react";
import { Sparkles, Copy, Check, Type, FileText, Tag, Mic } from "lucide-react";
import { generateTitleIdeas, generateDescription, generateTags, generateHooks } from "@/lib/api";
import { TitleIdea } from "@/lib/types";
import ScoreGauge from "@/components/common/ScoreGauge";

export default function AIStudioPage() {
  const [tab, setTab] = useState<"titles" | "description" | "tags" | "hooks">("titles");
  const [topic, setTopic] = useState("YouTube Automation 2026");
  const [targetKw, setTargetKw] = useState("youtube automation");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // States
  const [titles, setTitles] = useState<TitleIdea[]>([]);
  const [descResult, setDescResult] = useState<any | null>(null);
  const [tagsResult, setTagsResult] = useState<any | null>(null);
  const [hooksResult, setHooksResult] = useState<any[]>([]);

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const runGenerator = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    setError(null);
    try {
      if (tab === "titles") {
        const res = await generateTitleIdeas(topic, targetKw, 12);
        setTitles(res);
      } else if (tab === "description") {
        const res = await generateDescription(topic, [targetKw, "youtube automation tutorial"]);
        setDescResult(res);
      } else if (tab === "tags") {
        const res = await generateTags("How to Master YouTube Automation in 2026", topic, targetKw);
        setTagsResult(res);
      } else if (tab === "hooks") {
        const res = await generateHooks(topic, "Creators");
        setHooksResult(res);
      }
    } catch (err: any) {
      setError(err.message || "Failed to generate AI assets. In deterministic mode, check template inputs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Creator AI Studio</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Packaging generation powered by small local models (Qwen CPU) or deterministic heuristic templates.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 text-sm gap-6">
        {[
          { id: "titles", label: "Title Generator", icon: Type },
          { id: "description", label: "Description Builder", icon: FileText },
          { id: "tags", label: "Tag Generator", icon: Tag },
          { id: "hooks", label: "Retention Hooks", icon: Mic },
        ].map((t) => {
          const Icon = t.icon;
          const active = tab === t.id;
          return (
            <button
              key={t.id}
              onClick={() => setTab(t.id as any)}
              className={`flex items-center gap-2 pb-3 font-semibold transition-colors ${
                active ? "text-indigo-400 border-b-2 border-indigo-500" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{t.label}</span>
            </button>
          );
        })}
      </div>

      {/* Input controls */}
      <div className="glass-panel p-5 space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Video Topic</label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Topic name..."
              className="w-full bg-slate-900/90 border border-slate-700/80 rounded-lg px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Primary Target Keyword</label>
            <input
              type="text"
              value={targetKw}
              onChange={(e) => setTargetKw(e.target.value)}
              placeholder="e.g. 'youtube automation'"
              className="w-full bg-slate-900/90 border border-slate-700/80 rounded-lg px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
            />
          </div>
        </div>

        <button
          onClick={runGenerator}
          disabled={loading}
          className="px-5 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm flex items-center gap-2"
        >
          <Sparkles className="w-4 h-4" />
          <span>{loading ? "Generating..." : "Generate with Heuristic Scoring"}</span>
        </button>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm">
          {error}
        </div>
      )}

      {loading && (
        <div className="p-8 text-center glass-card rounded-xl border border-slate-800 space-y-2">
          <div className="inline-block w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-xs text-slate-400">Synthesizing packaging variations with deterministic scoring...</p>
        </div>
      )}

      {/* Title Generator Tab */}
      {tab === "titles" && titles.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {titles.map((t, idx) => (
            <div key={idx} className="glass-card p-4 rounded-xl border border-slate-800 space-y-3 flex flex-col justify-between">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="px-2 py-0.5 rounded bg-slate-800 text-indigo-300 text-[10px] font-bold">
                    {t.style}
                  </span>
                  <button
                    onClick={() => handleCopy(t.title, `title-${idx}`)}
                    className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
                  >
                    {copiedId === `title-${idx}` ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  </button>
                </div>
                <h3 className="text-sm font-bold text-white leading-snug">{t.title}</h3>
              </div>

              <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs">
                <div className="flex items-center gap-3">
                  <span className="text-slate-400">SEO Relevance: <strong className="text-slate-200">{t.seo_relevance_heuristic}%</strong></span>
                  <span className="text-slate-400">Curiosity: <strong className="text-cyan-400">{t.curiosity_heuristic}%</strong></span>
                </div>
                <span className="text-slate-500">{t.character_count} chars</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Description Builder Tab */}
      {tab === "description" && descResult && (
        <div className="glass-card p-6 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white">Generated Video Description</h3>
            <button
              onClick={() => handleCopy(descResult.full_description, "desc")}
              className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 flex items-center gap-1.5"
            >
              {copiedId === "desc" ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>Copy Description</span>
            </button>
          </div>
          <pre className="p-4 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-300 whitespace-pre-wrap font-sans leading-relaxed">
            {descResult.full_description}
          </pre>
        </div>
      )}

      {/* Tag Generator Tab */}
      {tab === "tags" && tagsResult && (
        <div className="glass-card p-6 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white">Generated Video Tags</h3>
            <button
              onClick={() => handleCopy([...tagsResult.primary_tags, ...tagsResult.secondary_tags, ...tagsResult.long_tail_tags].join(", "), "tags")}
              className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 flex items-center gap-1.5"
            >
              {copiedId === "tags" ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>Copy All Tags</span>
            </button>
          </div>

          <div className="space-y-3">
            <div>
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Primary Tags</span>
              <div className="flex flex-wrap gap-2 mt-1.5">
                {tagsResult.primary_tags.map((t: string, i: number) => (
                  <span key={i} className="px-2.5 py-1 rounded-md bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs">
                    {t}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Secondary Tags</span>
              <div className="flex flex-wrap gap-2 mt-1.5">
                {tagsResult.secondary_tags.map((t: string, i: number) => (
                  <span key={i} className="px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700 text-slate-300 text-xs">
                    {t}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Long-Tail Tags</span>
              <div className="flex flex-wrap gap-2 mt-1.5">
                {tagsResult.long_tail_tags.map((t: string, i: number) => (
                  <span key={i} className="px-2.5 py-1 rounded-md bg-cyan-500/10 border border-cyan-500/20 text-cyan-300 text-xs">
                    {t}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Retention Hooks Tab */}
      {tab === "hooks" && hooksResult.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {hooksResult.map((hook, i) => (
            <div key={i} className="glass-card p-5 rounded-xl border border-slate-800 space-y-3">
              <span className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 text-xs font-bold border border-purple-500/20">
                {hook.hook_type}
              </span>

              <div className="space-y-1">
                <span className="text-[11px] text-slate-400 font-semibold uppercase">First 3 Seconds:</span>
                <p className="text-xs font-bold text-white">&ldquo;{hook.first_3_seconds}&rdquo;</p>
              </div>

              <div className="space-y-1">
                <span className="text-[11px] text-slate-400 font-semibold uppercase">Next 15 Seconds:</span>
                <p className="text-xs text-slate-300 leading-relaxed">&ldquo;{hook.next_15_seconds}&rdquo;</p>
              </div>

              <div className="space-y-1 pt-2 border-t border-slate-800/80">
                <span className="text-[11px] text-indigo-400 font-semibold uppercase">Open Loop Retention Spark:</span>
                <p className="text-xs text-slate-400">&ldquo;{hook.open_loop}&rdquo;</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
