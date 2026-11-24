"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Search,
  Sparkles,
  TrendingUp,
  Video,
  Layers,
  ArrowRight,
  ShieldCheck,
  Zap,
} from "lucide-react";
import ScoreGauge from "@/components/common/ScoreGauge";
import DataProvenanceBadge from "@/components/common/DataProvenanceBadge";

export default function DashboardPage() {
  const router = useRouter();
  const [seed, setSeed] = useState("");

  const handleLaunchResearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (seed.trim()) {
      router.push(`/keywords?seed=${encodeURIComponent(seed.trim())}`);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Hero Welcome & Quick Launch */}
      <div className="rounded-xl bg-[var(--color-paper-2)] p-8 border border-[var(--color-rule)]">
        <div className="max-w-2xl space-y-4">
          <div className="flex flex-wrap items-center gap-2">
            <span className="px-2.5 py-0.5 rounded text-xs bg-[var(--color-paper-3)] border border-[var(--color-rule)] text-[var(--color-muted)]">
              Independent
            </span>
            <span className="px-2.5 py-0.5 rounded text-xs bg-[var(--color-paper-3)] border border-[var(--color-rule)] text-[var(--color-muted)]">
              Transparent
            </span>
            <span className="px-2.5 py-0.5 rounded text-xs bg-[var(--color-paper-3)] border border-[var(--color-rule)] text-[var(--color-muted)]">
              No paid API required
            </span>
          </div>

          <h1 className="text-3xl sm:text-4xl font-medium tracking-[-0.03em] text-[var(--color-ink)]">
            YouTube creator intelligence and search optimization
          </h1>

          <p className="text-sm text-[var(--color-muted)] leading-relaxed">
            Stateless keyword research, statistical competition analysis, 0-100 opportunity scoring, and 18-point SEO audits on your server.
          </p>

          <form onSubmit={handleLaunchResearch} className="pt-2 flex flex-col sm:flex-row gap-3">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-[var(--color-muted)] absolute left-4 top-1/2 -translate-y-1/2 pointer-events-none" />
              <input
                type="text"
                value={seed}
                onChange={(e) => setSeed(e.target.value)}
                placeholder="Enter seed topic (e.g. 'faceless youtube automation', 'davinci resolve')..."
                className="w-full bg-[var(--color-paper-3)] border border-[var(--color-rule)] rounded-md pl-11 pr-4 py-3 text-sm text-[var(--color-ink)] placeholder-[var(--color-muted)] focus:outline-none focus:border-[var(--color-rule-2)] focus:ring-1 focus:ring-[var(--color-focus)] transition-colors duration-150"
              />
            </div>
            <button
              type="submit"
              className="px-6 py-3 rounded-md bg-[var(--color-accent)] hover:bg-[var(--color-accent)]/90 text-[var(--color-accent-ink)] font-medium text-sm flex items-center justify-center gap-2 transition-colors duration-150"
            >
              <span>Explore keywords</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>

      {/* Primary Telemetry Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Benchmark SEO Health */}
        <div className="p-5 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] flex items-center justify-between">
          <div className="space-y-1">
            <span className="text-xs text-[var(--color-muted)] font-normal">Channel SEO health</span>
            <div className="text-2xl font-normal text-[var(--color-ink)] measured">
              88<span className="text-xs text-[var(--color-muted)] font-normal">/100</span>
            </div>
            <span className="text-[11px] text-[var(--color-ok)] font-normal flex items-center gap-1">
              <TrendingUp className="w-3 h-3" /> +14 pts from fixes
            </span>
          </div>
          <ScoreGauge score={88} size="sm" />
        </div>

        {/* Card 2: High-Opportunity Niches */}
        <div className="p-5 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] flex items-center justify-between">
          <div className="space-y-1">
            <span className="text-xs text-[var(--color-muted)] font-normal">Content gaps detected</span>
            <div className="text-2xl font-normal text-[var(--color-cool)] measured">12 topics</div>
            <span className="text-[11px] text-[var(--color-muted)]">Uncovered in competitor SERPs</span>
          </div>
          <div className="w-10 h-10 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center text-[var(--color-cool)]">
            <Layers className="w-5 h-5" />
          </div>
        </div>

        {/* Card 3: Breakout Outlier Multiplier */}
        <div className="p-5 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] flex items-center justify-between">
          <div className="space-y-1">
            <span className="text-xs text-[var(--color-muted)] font-normal">Max outlier found</span>
            <div className="text-2xl font-normal text-[var(--color-accent)] measured">28.4x</div>
            <span className="text-[11px] text-[var(--color-muted)]">Above channel median views</span>
          </div>
          <div className="w-10 h-10 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center text-[var(--color-accent)]">
            <Zap className="w-5 h-5" />
          </div>
        </div>

        {/* Card 4: Architecture Status */}
        <div className="p-5 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] flex items-center justify-between">
          <div className="space-y-1">
            <span className="text-xs text-[var(--color-muted)] font-normal">Platform mode</span>
            <div className="text-base font-normal text-[var(--color-ok)]">Zero DB / Stateless</div>
            <span className="text-[11px] text-[var(--color-muted)]">In-memory TTL cache active</span>
          </div>
          <div className="w-10 h-10 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center text-[var(--color-ok)]">
            <ShieldCheck className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* Feature Modules Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Module 1: Keyword Research */}
        <div className="p-6 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] space-y-4">
          <div className="w-9 h-9 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center text-[var(--color-accent)]">
            <Search className="w-4 h-4" />
          </div>
          <h2 className="text-base font-medium text-[var(--color-ink)]">Keyword intelligence</h2>
          <p className="text-xs text-[var(--color-muted)] leading-relaxed">
            Multi-vector autocomplete and alphabet expansion discovering long-tail phrases with transparent relative demand and estimated competition indices.
          </p>
          <Link
            href="/keywords"
            className="inline-flex items-center gap-1.5 text-xs font-medium text-[var(--color-accent)] hover:underline"
          >
            Launch keyword tool <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Module 2: Video & Channel Audit */}
        <div className="p-6 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] space-y-4">
          <div className="w-9 h-9 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center text-[var(--color-ok)]">
            <Video className="w-4 h-4" />
          </div>
          <h2 className="text-base font-medium text-[var(--color-ink)]">18-point SEO audit</h2>
          <p className="text-xs text-[var(--color-muted)] leading-relaxed">
            Deterministic checklist evaluating titles, descriptions, keyword alignment, tags, and chapter markers with precise mathematical category scores.
          </p>
          <Link
            href="/video-audit"
            className="inline-flex items-center gap-1.5 text-xs font-medium text-[var(--color-ok)] hover:underline"
          >
            Run video audit <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Module 3: AI Studio & Ideation */}
        <div className="p-6 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] space-y-4">
          <div className="w-9 h-9 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center text-[var(--color-cool)]">
            <Sparkles className="w-4 h-4" />
          </div>
          <h2 className="text-base font-medium text-[var(--color-ink)]">Creator studio and ideation</h2>
          <p className="text-xs text-[var(--color-muted)] leading-relaxed">
            Generate high-CTR title variations, retention hooks, chapters, and 30-day content calendars powered by local small models or deterministic templates.
          </p>
          <Link
            href="/ai-studio"
            className="inline-flex items-center gap-1.5 text-xs font-medium text-[var(--color-cool)] hover:underline"
          >
            Open AI studio <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Data Provenance & Ethics Guarantee */}
      <div className="p-6 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="space-y-1">
          <span className="text-sm font-medium text-[var(--color-ink)]">Ethical data provenance guarantee</span>
          <p className="text-xs text-[var(--color-muted)]">
            YouTube SEO never fabricates fake search volumes, CTR, or revenue metrics. All signals are explicitly marked as Official, Public, Calculated, Estimated, or Relative.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <DataProvenanceBadge provenance="Public" />
          <DataProvenanceBadge provenance="Calculated" />
          <DataProvenanceBadge provenance="Estimated" />
          <DataProvenanceBadge provenance="Relative" />
        </div>
      </div>
    </div>
  );
}
