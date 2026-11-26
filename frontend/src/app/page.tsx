"use client";

import React, { useState, useEffect } from "react";
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
  Info,
  UserCheck,
  CheckCircle2,
  KeyRound,
  BookOpen,
} from "lucide-react";
import ScoreGauge from "@/components/common/ScoreGauge";
import DataProvenanceBadge from "@/components/common/DataProvenanceBadge";
import AeoFaqSection from "@/components/seo/AeoFaqSection";
import { fetchWorkspaceAudits, fetchWorkspaceCompetitors, fetchWorkspaceKeywordProjects } from "@/lib/api";

export default function DashboardPage() {
  const router = useRouter();
  const [seed, setSeed] = useState("");
  const [auditTarget, setAuditTarget] = useState("");
  const [realAudits, setRealAudits] = useState<any[]>([]);
  const [realCompetitors, setRealCompetitors] = useState<any[]>([]);
  const [realKeywords, setRealKeywords] = useState<any[]>([]);
  const [hasRealData, setHasRealData] = useState(false);

  useEffect(() => {
    async function loadWorkspace() {
      try {
        const [audits, comps, kws] = await Promise.all([
          fetchWorkspaceAudits(),
          fetchWorkspaceCompetitors(),
          fetchWorkspaceKeywordProjects(),
        ]);
        if (audits && audits.length > 0) setRealAudits(audits);
        if (comps && comps.length > 0) setRealCompetitors(comps);
        if (kws && kws.length > 0) setRealKeywords(kws);
        if ((audits && audits.length > 0) || (comps && comps.length > 0) || (kws && kws.length > 0)) {
          setHasRealData(true);
        }
      } catch {
        // Fall back gracefully to sample demo view with explicit disclosure
      }
    }
    loadWorkspace();
  }, []);

  const handleLaunchResearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (seed.trim()) {
      router.push(`/keywords?seed=${encodeURIComponent(seed.trim())}`);
    }
  };

  const handleLaunchAudit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!auditTarget.trim()) return;
    const target = auditTarget.trim();
    if (target.includes("youtube.com/watch") || target.includes("youtu.be/")) {
      router.push(`/video-audit?url=${encodeURIComponent(target)}`);
    } else {
      router.push(`/channel-audit?channel=${encodeURIComponent(target)}`);
    }
  };

  const latestAuditScore = realAudits.length > 0 ? realAudits[0].overall_score : null;

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Hero Welcome & Quick Launch */}
      <div className="rounded-xl bg-[var(--color-paper-2)] p-6 sm:p-8 border border-[var(--color-rule)]">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          {/* Left Column: Hero Text & Search */}
          <div className="lg:col-span-7 space-y-4">
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
                className="px-6 py-3 rounded-md bg-[var(--color-accent)] hover:bg-[var(--color-accent)]/90 text-[var(--color-accent-ink)] font-medium text-sm flex items-center justify-center gap-2 transition-colors duration-150 shrink-0"
              >
                <span>Explore keywords</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>
          </div>

          {/* Right Column: API Integration & Setup Guide Card */}
          <div className="lg:col-span-5">
            <div className="rounded-xl bg-[var(--color-paper-3)] border border-[var(--color-rule)] p-5 space-y-4 hover:border-[var(--color-accent)]/50 transition-all duration-200 shadow-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-lg bg-[var(--color-accent)]/10 text-[var(--color-accent)] flex items-center justify-center">
                    <KeyRound className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-xs font-semibold uppercase tracking-wider text-[var(--color-ink)]">
                      API Integration Guide
                    </h3>
                    <p className="text-[11px] text-[var(--color-muted)]">Official YouTube & Free AI</p>
                  </div>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                  100% Optional
                </span>
              </div>

              <div className="space-y-2 text-xs text-[var(--color-muted)]">
                <p className="leading-relaxed text-[11px]">
                  Want higher rate limits and deeper AI Studio suggestions? Connect your own free keys:
                </p>
                <div className="space-y-1.5 pl-0.5 pt-0.5">
                  <div className="flex items-center gap-2 text-[var(--color-ink)] text-xs">
                    <CheckCircle2 className="w-3.5 h-3.5 text-red-500 shrink-0" />
                    <span><strong>YouTube API v3:</strong> Free 10,000 units/day</span>
                  </div>
                  <div className="flex items-center gap-2 text-[var(--color-ink)] text-xs">
                    <CheckCircle2 className="w-3.5 h-3.5 text-blue-400 shrink-0" />
                    <span><strong>Google Gemini:</strong> Free cloud AI (15 RPM)</span>
                  </div>
                  <div className="flex items-center gap-2 text-[var(--color-ink)] text-xs">
                    <CheckCircle2 className="w-3.5 h-3.5 text-purple-400 shrink-0" />
                    <span><strong>Ollama / Local:</strong> Zero-cost private AI</span>
                  </div>
                </div>
              </div>

              <div className="pt-1 flex flex-col sm:flex-row gap-2">
                <Link
                  href="/api-setup"
                  className="flex-1 py-2 px-3 rounded-md bg-[var(--color-paper-2)] border border-[var(--color-rule-2)] hover:border-[var(--color-accent)] text-xs font-medium text-[var(--color-ink)] flex items-center justify-center gap-1.5 transition-colors"
                >
                  <BookOpen className="w-3.5 h-3.5 text-[var(--color-accent)]" />
                  <span>How to Add API (Guide)</span>
                </Link>
                <Link
                  href="/settings"
                  className="py-2 px-3.5 rounded-md bg-[var(--color-paper-2)] hover:bg-[var(--color-paper-1)] border border-[var(--color-rule)] text-xs text-[var(--color-muted)] hover:text-[var(--color-ink)] flex items-center justify-center transition-colors"
                >
                  <span>Settings</span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Real vs Sample Data Provenance Banner */}
      {!hasRealData && (
        <div className="p-3.5 rounded-lg bg-amber-500/10 border border-amber-500/25 flex items-center justify-between text-xs text-amber-300">
          <div className="flex items-center gap-2">
            <Info className="w-4 h-4 shrink-0" />
            <span>
              <strong>Sample Demo Showcase:</strong> The telemetry below displays illustrative baseline benchmarks. Run a live video or channel audit to replace them with your channel&apos;s real-time calculated signals.
            </span>
          </div>
          <DataProvenanceBadge provenance="Sample Data" />
        </div>
      )}

      {/* Primary Telemetry Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Benchmark SEO Health */}
        <div className="p-5 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] flex items-center justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xs text-[var(--color-muted)] font-normal">
                {hasRealData && latestAuditScore ? "Latest video audit score" : "Benchmark channel SEO health"}
              </span>
              <DataProvenanceBadge provenance={hasRealData && latestAuditScore ? "Calculated" : "Sample Data"} />
            </div>
            <div className="text-2xl font-normal text-[var(--color-ink)] measured">
              {latestAuditScore !== null ? latestAuditScore : 88}
              <span className="text-xs text-[var(--color-muted)] font-normal">/100</span>
            </div>
            <span className="text-[11px] text-[var(--color-ok)] font-normal flex items-center gap-1">
              <TrendingUp className="w-3 h-3" />
              {hasRealData ? "Live verified calculation" : "Sample baseline standard"}
            </span>
          </div>
          <ScoreGauge score={latestAuditScore !== null ? latestAuditScore : 88} size="sm" />
        </div>

        {/* Card 2: Tracked Competitors / Content Gaps */}
        <div className="p-5 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] flex items-center justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xs text-[var(--color-muted)] font-normal">
                {hasRealData ? "Watchlist competitors" : "Content gaps detected"}
              </span>
              <DataProvenanceBadge provenance={hasRealData ? "Public" : "Sample Data"} />
            </div>
            <div className="text-2xl font-normal text-[var(--color-cool)] measured">
              {hasRealData ? `${realCompetitors.length} channels` : "12 topics"}
            </div>
            <span className="text-[11px] text-[var(--color-muted)]">
              {hasRealData ? "Active competitor channels" : "Sample benchmark gap analysis"}
            </span>
          </div>
          <div className="w-10 h-10 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center text-[var(--color-cool)]">
            <Layers className="w-5 h-5" />
          </div>
        </div>

        {/* Card 3: Outlier Multiplier / Research History */}
        <div className="p-5 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] flex items-center justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xs text-[var(--color-muted)] font-normal">
                {hasRealData ? "Saved keyword queries" : "Max outlier multiplier"}
              </span>
              <DataProvenanceBadge provenance={hasRealData ? "Calculated" : "Sample Data"} />
            </div>
            <div className="text-2xl font-normal text-[var(--color-accent)] measured">
              {hasRealData ? `${realKeywords.length} seeds` : "28.4x"}
            </div>
            <span className="text-[11px] text-[var(--color-muted)]">
              {hasRealData ? "Researched projects stored" : "Sample above channel median"}
            </span>
          </div>
          <div className="w-10 h-10 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center text-[var(--color-accent)]">
            <Zap className="w-5 h-5" />
          </div>
        </div>

        {/* Card 4: Architecture Status */}
        <div className="p-5 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] flex items-center justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xs text-[var(--color-muted)] font-normal">Platform mode</span>
              <DataProvenanceBadge provenance="Calculated" />
            </div>
            <div className="text-base font-normal text-[var(--color-ok)]">Stateless Core</div>
            <span className="text-[11px] text-[var(--color-muted)]">In-memory TTL cache active</span>
          </div>
          <div className="w-10 h-10 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center text-[var(--color-ok)]">
            <ShieldCheck className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* Quick Live Audit Tool */}
      <div className="p-6 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-base font-medium text-[var(--color-ink)]">Run Real Live SEO Audit</h2>
            <p className="text-xs text-[var(--color-muted)]">
              Analyze any public YouTube video or channel URL for immediate 18-point score and actionable checklist.
            </p>
          </div>
          <DataProvenanceBadge provenance="Public" />
        </div>

        <form onSubmit={handleLaunchAudit} className="flex flex-col sm:flex-row gap-3 pt-1">
          <input
            type="text"
            value={auditTarget}
            onChange={(e) => setAuditTarget(e.target.value)}
            placeholder="Paste YouTube Video URL (https://www.youtube.com/watch?v=...) or Channel handle (@channel)..."
            className="flex-1 bg-[var(--color-paper-3)] border border-[var(--color-rule)] rounded-md px-4 py-2.5 text-sm text-[var(--color-ink)] placeholder-[var(--color-muted)] focus:outline-none focus:border-[var(--color-rule-2)]"
          />
          <button
            type="submit"
            className="px-5 py-2.5 rounded-md bg-[var(--color-paper-3)] hover:bg-[var(--color-rule)] border border-[var(--color-rule-2)] text-[var(--color-ink)] text-sm font-medium flex items-center justify-center gap-2 transition-colors"
          >
            <Video className="w-4 h-4 text-[var(--color-accent)]" />
            <span>Audit Now</span>
          </button>
        </form>
      </div>

      {/* Feature Modules Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Module 1: Keyword Research */}
        <div className="p-6 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] space-y-4">
          <div className="flex items-center justify-between">
            <div className="w-9 h-9 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center text-[var(--color-accent)]">
              <Search className="w-4 h-4" />
            </div>
            <DataProvenanceBadge provenance="Public" />
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
          <div className="flex items-center justify-between">
            <div className="w-9 h-9 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center text-[var(--color-ok)]">
              <Video className="w-4 h-4" />
            </div>
            <DataProvenanceBadge provenance="Calculated" />
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
          <div className="flex items-center justify-between">
            <div className="w-9 h-9 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center text-[var(--color-cool)]">
              <Sparkles className="w-4 h-4" />
            </div>
            <DataProvenanceBadge provenance="AI Recommendation" />
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

      {/* Answer Engine Optimization (AEO) FAQ & Knowledge Base */}
      <AeoFaqSection />

      {/* Data Provenance & Ethics Guarantee */}
      <div className="p-6 rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="space-y-1">
          <span className="text-sm font-medium text-[var(--color-ink)]">Ethical data provenance guarantee</span>
          <p className="text-xs text-[var(--color-muted)]">
            YouTube SEO never fabricates fake search volumes, CTR, or revenue metrics. All signals are explicitly marked as Official, Public, Calculated, Estimated, Relative, or Sample Data.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <DataProvenanceBadge provenance="Sample Data" />
          <DataProvenanceBadge provenance="Public" />
          <DataProvenanceBadge provenance="Calculated" />
          <DataProvenanceBadge provenance="Estimated" />
          <DataProvenanceBadge provenance="AI Recommendation" />
        </div>
      </div>
    </div>
  );
}
