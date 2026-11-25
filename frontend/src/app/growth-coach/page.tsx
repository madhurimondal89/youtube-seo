"use client";

import React, { useState } from "react";
import {
  Sparkles,
  Calendar,
  Compass,
  CheckCircle2,
  Copy,
  Download,
  BookOpen,
  ArrowRight,
  TrendingUp,
  Video,
  Layers,
  FileText,
} from "lucide-react";
import { fetchGrowthStrategy } from "@/lib/api";
import { GrowthStrategyResponse } from "@/lib/types";

const NICHE_PRESETS = [
  { label: "Bengali Mystery & History", niche: "Bengali Mystery and History", lang: "Bengali" },
  { label: "Faceless YouTube Automation", niche: "Faceless YouTube Automation and AI", lang: "English" },
  { label: "Tech & Coding Tutorials", niche: "Web Development & Programming Tutorials", lang: "English" },
  { label: "True Crime & Cold Cases", niche: "True Crime and Unsolved Mysteries", lang: "English" },
  { label: "Personal Finance & Investing", niche: "Personal Finance for Beginners", lang: "English" },
  { label: "Gaming Lore & Walkthroughs", niche: "Gaming Lore and Mechanics Breakdown", lang: "English" },
];

export default function GrowthCoachPage() {
  const [niche, setNiche] = useState("Bengali Mystery and History");
  const [channelName, setChannelName] = useState("");
  const [language, setLanguage] = useState("Bengali");
  const [customKeywords, setCustomKeywords] = useState("");
  const [channelContext, setChannelContext] = useState("");
  const [showAdvancedContext, setShowAdvancedContext] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [strategy, setStrategy] = useState<GrowthStrategyResponse | null>(null);
  const [copied, setCopied] = useState(false);

  const handleGenerate = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!niche.trim()) return;

    setError(null);
    setLoading(true);

    const kwList = customKeywords
      .split(",")
      .map((k) => k.trim())
      .filter(Boolean);

    try {
      const res = await fetchGrowthStrategy(
        niche.trim(),
        channelName.trim() || undefined,
        language,
        kwList.length > 0 ? kwList : undefined,
        undefined,
        channelContext.trim() || undefined
      );
      setStrategy(res);
    } catch (err: any) {
      setError(err.message || "Failed to generate growth strategy");
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    if (!strategy) return;
    let text = `# 30-Day Growth Strategy: ${strategy.niche}\n\n`;
    text += `**Channel**: ${strategy.channel_name || "Creator"}\n`;
    text += `**Language**: ${strategy.language}\n`;
    text += `**Summary**: ${strategy.executive_summary}\n\n`;

    strategy.weeks.forEach((w) => {
      text += `## Week ${w.week_number}: ${w.theme}\nObjective: ${w.milestone_objective}\n\n`;
      w.videos.forEach((v) => {
        text += `### Day ${v.day}: ${v.title} (${v.format})\n`;
        text += `- Keyword: ${v.target_keyword}\n`;
        text += `- Hook: "${v.hook_script}"\n`;
        text += `- Thumbnail: ${v.thumbnail_concept}\n`;
        text += `- Structure: ${v.script_structure.join(" -> ")}\n\n`;
      });
    });

    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="max-w-[1500px] mx-auto space-y-6">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-2xl font-medium tracking-tight text-[var(--color-ink)]">
          AI Creator Growth Coach &amp; 30-Day Strategy Engine
        </h1>
        <p className="text-xs text-[var(--color-muted)]">
          Tailored content calendars, high-retention hook scripts, thumbnail concepts, and milestone metrics for high-growth niches.
        </p>
      </div>

      {/* Input Form & Preset Chips */}
      <div className="panel-console p-6 space-y-4">
        {/* Presets */}
        <div className="space-y-1.5">
          <span className="text-xs text-[var(--color-muted)]">Quick Niche Presets:</span>
          <div className="flex flex-wrap gap-2">
            {NICHE_PRESETS.map((p, i) => (
              <button
                key={i}
                type="button"
                onClick={() => {
                  setNiche(p.niche);
                  setLanguage(p.lang);
                }}
                className={`px-2.5 py-1 rounded text-xs transition-colors duration-150 ${
                  niche === p.niche
                    ? "bg-[var(--color-accent)] text-[var(--color-accent-ink)] font-medium"
                    : "bg-[var(--color-paper-3)] border border-[var(--color-rule)] text-[var(--color-muted)] hover:text-[var(--color-ink)]"
                }`}
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleGenerate} className="grid grid-cols-1 md:grid-cols-4 gap-3 pt-2">
          <div className="md:col-span-2 space-y-1">
            <label className="text-xs text-[var(--color-muted)]">Target Niche &amp; Subject</label>
            <input
              type="text"
              value={niche}
              onChange={(e) => setNiche(e.target.value)}
              placeholder="e.g. Bengali Mystery and History, Faceless AI Tools..."
              className="w-full bg-[var(--color-paper-3)] border border-[var(--color-rule)] rounded-md px-3 py-2 text-xs text-[var(--color-ink)] placeholder-[var(--color-muted)] focus:outline-none focus:border-[var(--color-rule-2)]"
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs text-[var(--color-muted)]">Channel Name (Optional)</label>
            <input
              type="text"
              value={channelName}
              onChange={(e) => setChannelName(e.target.value)}
              placeholder="e.g. Rahasya Golpo"
              className="w-full bg-[var(--color-paper-3)] border border-[var(--color-rule)] rounded-md px-3 py-2 text-xs text-[var(--color-ink)] placeholder-[var(--color-muted)] focus:outline-none focus:border-[var(--color-rule-2)]"
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs text-[var(--color-muted)]">Primary Language</label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full bg-[var(--color-paper-3)] border border-[var(--color-rule)] rounded-md px-3 py-2 text-xs text-[var(--color-ink)] focus:outline-none focus:border-[var(--color-rule-2)]"
            >
              <option value="English">English</option>
              <option value="Bengali">Bengali (বাংলা)</option>
              <option value="Hindi">Hindi (हिन्दी)</option>
              <option value="Spanish">Spanish</option>
              <option value="Portuguese">Portuguese</option>
            </select>
          </div>

          <div className="md:col-span-4">
            <button
              type="button"
              onClick={() => setShowAdvancedContext(!showAdvancedContext)}
              className="text-xs text-[var(--color-accent)] hover:underline inline-flex items-center gap-1.5"
            >
              <span>{showAdvancedContext ? "– Hide Context & Performance Signals" : "+ Add Context & Validated Keywords (Optional)"}</span>
            </button>
          </div>

          {showAdvancedContext && (
            <>
              <div className="md:col-span-2 space-y-1">
                <label className="text-xs text-[var(--color-muted)]">Validated Research Keywords (comma-separated)</label>
                <input
                  type="text"
                  value={customKeywords}
                  onChange={(e) => setCustomKeywords(e.target.value)}
                  placeholder="e.g. bangla history documentary, unsolved cases, british archives"
                  className="w-full bg-[var(--color-paper-3)] border border-[var(--color-rule)] rounded-md px-3 py-2 text-xs text-[var(--color-ink)] placeholder-[var(--color-muted)] focus:outline-none focus:border-[var(--color-rule-2)]"
                />
              </div>

              <div className="md:col-span-2 space-y-1">
                <label className="text-xs text-[var(--color-muted)]">Channel Context &amp; High-Retention Topics</label>
                <input
                  type="text"
                  value={channelContext}
                  onChange={(e) => setChannelContext(e.target.value)}
                  placeholder="e.g. Median 50K views, top outliers in investigative documentaries"
                  className="w-full bg-[var(--color-paper-3)] border border-[var(--color-rule)] rounded-md px-3 py-2 text-xs text-[var(--color-ink)] placeholder-[var(--color-muted)] focus:outline-none focus:border-[var(--color-rule-2)]"
                />
              </div>
            </>
          )}

          <div className="md:col-span-4 pt-1">
            <button
              type="submit"
              disabled={loading || !niche.trim()}
              className="px-5 py-2.5 rounded-md bg-[var(--color-accent)] hover:bg-[var(--color-accent)]/90 text-[var(--color-accent-ink)] font-medium text-xs flex items-center justify-center gap-2 transition-colors duration-150 disabled:opacity-50"
            >
              <Sparkles className="w-4 h-4" />
              <span>{loading ? "Generating 30-Day Strategy..." : "Generate 30-Day Growth Strategy"}</span>
            </button>
          </div>
        </form>
      </div>

      {error && (
        <div className="p-4 rounded-md bg-[var(--color-bad-soft)] border border-[var(--color-bad)]/40 text-xs text-[var(--color-bad)]">
          {error}
        </div>
      )}

      {/* Strategy Display */}
      {strategy && (
        <div className="space-y-6">
          {/* Executive Overview */}
          <div className="panel-console p-6 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[var(--color-rule)] pb-4">
              <div>
                <span className="text-xs text-[var(--color-accent)] font-medium">
                  Strategy Overview · {strategy.language}
                </span>
                <h2 className="text-lg font-medium text-[var(--color-ink)]">
                  30-Day Roadmap: {strategy.niche}
                </h2>
              </div>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={copyToClipboard}
                  className="px-3 py-1.5 rounded bg-[var(--color-paper-3)] border border-[var(--color-rule)] text-xs text-[var(--color-ink)] hover:bg-[var(--color-rule)] flex items-center gap-1.5"
                >
                  <Copy className="w-3.5 h-3.5" />
                  <span>{copied ? "Copied!" : "Copy Markdown"}</span>
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="space-y-1">
                <span className="text-[var(--color-muted)] font-medium">Executive Strategy:</span>
                <p className="text-[var(--color-ink-2)] leading-relaxed">{strategy.executive_summary}</p>
              </div>
              <div className="space-y-1">
                <span className="text-[var(--color-muted)] font-medium">Target Audience Persona:</span>
                <p className="text-[var(--color-ink-2)] leading-relaxed">{strategy.target_audience_profile}</p>
              </div>
            </div>
          </div>

          {/* 4 Weekly Breakdown Modules */}
          <div className="space-y-4">
            <span className="text-sm font-medium text-[var(--color-ink)]">
              Four-Week Production Schedule
            </span>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {strategy.weeks.map((week) => (
                <div key={week.week_number} className="panel-console p-5 space-y-4">
                  <div className="flex items-center justify-between border-b border-[var(--color-rule)] pb-3">
                    <div>
                      <span className="text-[11px] text-[var(--color-accent)] font-medium">
                        WEEK {week.week_number}
                      </span>
                      <h3 className="text-sm font-medium text-[var(--color-ink)]">{week.theme}</h3>
                    </div>
                    <span className="text-[11px] text-[var(--color-muted)] bg-[var(--color-paper-3)] px-2 py-0.5 rounded border border-[var(--color-rule)]">
                      {week.milestone_objective}
                    </span>
                  </div>

                  {/* Videos */}
                  <div className="space-y-3">
                    {week.videos.map((vid, vIdx) => (
                      <div
                        key={vIdx}
                        className="p-3.5 rounded bg-[var(--color-paper-3)] border border-[var(--color-rule)] space-y-2"
                      >
                        <div className="flex items-center justify-between text-xs">
                          <span className="font-medium text-[var(--color-accent)] measured">
                            Day {vid.day}
                          </span>
                          <span className="text-[11px] text-[var(--color-cool)] bg-[var(--color-paper-2)] px-2 py-0.5 rounded">
                            {vid.format}
                          </span>
                        </div>

                        <div className="text-xs font-medium text-[var(--color-ink)]">
                          {vid.title}
                        </div>

                        <div className="text-[11px] text-[var(--color-muted)]">
                          <span className="text-[var(--color-ink)] font-normal">Keyword:</span>{" "}
                          <span className="measured text-[var(--color-accent)]">{vid.target_keyword}</span>
                        </div>

                        <div className="text-[11px] text-[var(--color-muted)] bg-[var(--color-paper-2)] p-2 rounded border border-[var(--color-rule)]/50">
                          <span className="text-[var(--color-ink)] font-normal">Retention Hook:</span>{" "}
                          &quot;{vid.hook_script}&quot;
                        </div>

                        <div className="text-[11px] text-[var(--color-muted)]">
                          <span className="text-[var(--color-ink)] font-normal">Thumbnail Concept:</span>{" "}
                          {vid.thumbnail_concept}
                        </div>

                        <div className="pt-1">
                          <span className="text-[10px] text-[var(--color-muted)] block mb-1">
                            Script Structure:
                          </span>
                          <div className="flex flex-wrap gap-1">
                            {vid.script_structure.map((step, sIdx) => (
                              <span
                                key={sIdx}
                                className="px-1.5 py-0.5 rounded text-[10px] bg-[var(--color-paper)] border border-[var(--color-rule)] text-[var(--color-muted)]"
                              >
                                {step}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Publishing Checklist & Weekly Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="panel-console p-5 space-y-3">
              <span className="text-sm font-medium text-[var(--color-ink)]">
                Algorithmic Publishing Checklist
              </span>
              <ul className="space-y-2 text-xs text-[var(--color-muted)]">
                {strategy.publishing_checklist.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-[var(--color-ok)] mt-0.5 flex-shrink-0" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="panel-console p-5 space-y-3">
              <span className="text-sm font-medium text-[var(--color-ink)]">
                Key Performance Review Benchmarks
              </span>
              <ul className="space-y-2 text-xs text-[var(--color-muted)]">
                {strategy.weekly_review_metrics.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <TrendingUp className="w-3.5 h-3.5 text-[var(--color-cool)] mt-0.5 flex-shrink-0" />
                    <span>{item}</span>
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
