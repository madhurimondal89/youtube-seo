"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  KeyRound,
  ExternalLink,
  CheckCircle2,
  Copy,
  Check,
  Sparkles,
  Cpu,
  Video,
  Zap,
  ShieldCheck,
  Terminal,
  ArrowRight,
  Info,
  Server,
  Layers,
  ArrowLeft,
  Settings,
} from "lucide-react";

export default function ApiSetupPage() {
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2500);
  };

  return (
    <div className="max-w-5xl mx-auto space-y-10 pb-16">
      {/* Top Header & Navigation */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[var(--color-rule)] pb-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Link
              href="/"
              className="text-xs text-[var(--color-muted)] hover:text-[var(--color-ink)] flex items-center gap-1 transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              Back to Dashboard
            </Link>
            <span className="text-[var(--color-rule)]">/</span>
            <span className="text-xs text-[var(--color-accent)] font-medium">Documentation</span>
          </div>
          <h1 className="text-3xl font-semibold tracking-tight text-[var(--color-ink)] flex items-center gap-3">
            <KeyRound className="w-8 h-8 text-[var(--color-accent)]" />
            Complete API Setup & Integration Guide
          </h1>
          <p className="text-sm text-[var(--color-muted)] mt-1.5 max-w-2xl leading-relaxed">
            Learn step-by-step how to get free official YouTube Data API keys and connect fast AI models
            (Gemini, Groq, Ollama, LM Studio) to unlock unlimited performance.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <Link
            href="/settings"
            className="px-4 py-2.5 rounded-lg bg-[var(--color-accent)] hover:bg-[var(--color-accent)]/90 text-[var(--color-accent-ink)] font-medium text-sm flex items-center gap-2 shadow-sm transition-all"
          >
            <Settings className="w-4 h-4" />
            <span>Open Settings</span>
          </Link>
        </div>
      </div>

      {/* Important Clarification Banner */}
      <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-sm flex items-start gap-3">
        <ShieldCheck className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <div className="font-medium text-emerald-200">
            Good News: YouTube SEO Works Without Any Paid APIs!
          </div>
          <p className="text-xs text-emerald-300/90 leading-relaxed">
            TubePilot already includes a <strong>Deterministic / Stateless Engine</strong> that runs keyword analysis,
            competition metrics, and 18-point SEO audits out of the box with zero setup. Adding an API key is completely
            optional and gives you higher rate limits and deeper AI-powered suggestions.
          </p>
        </div>
      </div>

      {/* Navigation Quick Jump Tabs */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <a
          href="#youtube-api"
          className="p-3 rounded-lg bg-[var(--color-paper-2)] border border-[var(--color-rule)] hover:border-[var(--color-accent)]/50 transition-all text-xs font-medium flex items-center gap-2.5 text-[var(--color-ink)]"
        >
          <svg className="w-4 h-4 text-red-500 fill-current shrink-0" viewBox="0 0 24 24">
            <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
          </svg>
          <span>YouTube Data API v3</span>
        </a>
        <a
          href="#gemini-api"
          className="p-3 rounded-lg bg-[var(--color-paper-2)] border border-[var(--color-rule)] hover:border-[var(--color-accent)]/50 transition-all text-xs font-medium flex items-center gap-2.5 text-[var(--color-ink)]"
        >
          <Sparkles className="w-4 h-4 text-blue-400 shrink-0" />
          <span>Google Gemini (Free)</span>
        </a>
        <a
          href="#groq-api"
          className="p-3 rounded-lg bg-[var(--color-paper-2)] border border-[var(--color-rule)] hover:border-[var(--color-accent)]/50 transition-all text-xs font-medium flex items-center gap-2.5 text-[var(--color-ink)]"
        >
          <Zap className="w-4 h-4 text-amber-400 shrink-0" />
          <span>Groq Cloud (Fast)</span>
        </a>
        <a
          href="#local-ai"
          className="p-3 rounded-lg bg-[var(--color-paper-2)] border border-[var(--color-rule)] hover:border-[var(--color-accent)]/50 transition-all text-xs font-medium flex items-center gap-2.5 text-[var(--color-ink)]"
        >
          <Server className="w-4 h-4 text-purple-400 shrink-0" />
          <span>Ollama / Local AI</span>
        </a>
      </div>

      {/* SECTION 1: YouTube Data API v3 */}
      <section id="youtube-api" className="rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] p-6 sm:p-8 space-y-6">
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-500/10 border border-red-500/20 flex items-center justify-center">
              <svg className="w-6 h-6 text-red-500 fill-current" viewBox="0 0 24 24">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
              </svg>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-semibold text-[var(--color-ink)]">
                  1. YouTube Data API v3 (Official Google API)
                </h2>
                <span className="px-2 py-0.5 rounded text-[11px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  Free 10,000 units/day
                </span>
              </div>
              <p className="text-xs text-[var(--color-muted)] mt-0.5">
                Official Google Cloud API for deep channel statistics, verified video metadata, and real-time tags.
              </p>
            </div>
          </div>

          <a
            href="https://console.cloud.google.com/apis/library/youtube.googleapis.com"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3.5 py-1.5 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] hover:border-[var(--color-rule-2)] text-xs text-[var(--color-ink)] flex items-center gap-1.5 transition-colors"
          >
            <span>Google Cloud Console</span>
            <ExternalLink className="w-3 h-3 text-[var(--color-muted)]" />
          </a>
        </div>

        <div className="space-y-4">
          <h3 className="text-sm font-medium text-[var(--color-ink)] flex items-center gap-2">
            <span>Step-by-Step Instructions:</span>
          </h3>

          <ol className="space-y-3.5 text-xs text-[var(--color-muted)] leading-relaxed list-decimal list-inside">
            <li className="pl-1">
              Go to{" "}
              <a
                href="https://console.cloud.google.com/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-[var(--color-accent)] hover:underline inline-flex items-center gap-0.5"
              >
                Google Cloud Console <ExternalLink className="w-2.5 h-2.5" />
              </a>{" "}
              and sign in with your Google account.
            </li>
            <li className="pl-1">
              Click the project dropdown at the top and select <strong>&quot;New Project&quot;</strong> (name it e.g. <code>My YouTube Tools</code>).
            </li>
            <li className="pl-1">
              In the search bar at the top, search for <strong>&quot;YouTube Data API v3&quot;</strong> and click <strong>&quot;Enable&quot;</strong>.
            </li>
            <li className="pl-1">
              Navigate to <strong>APIs & Services &gt; Credentials</strong> on the left sidebar.
            </li>
            <li className="pl-1">
              Click <strong>&quot;+ CREATE CREDENTIALS&quot;</strong> at the top &gt; select <strong>&quot;API Key&quot;</strong>.
            </li>
            <li className="pl-1">
              Copy your generated API Key (it looks like <code>AIzaSy...</code>).
            </li>
            <li className="pl-1">
              Open your{" "}
              <Link href="/settings" className="text-[var(--color-accent)] hover:underline font-medium">
                TubePilot Settings Page
              </Link>
              , switch <strong>YouTube Data Provider</strong> to <em>&quot;Official YouTube Data API v3&quot;</em>, paste your key, and click <strong>Save Settings</strong>!
            </li>
          </ol>
        </div>

        <div className="p-3.5 rounded-lg bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-between text-xs">
          <div className="flex items-center gap-2 text-[var(--color-muted)]">
            <Info className="w-4 h-4 text-sky-400 shrink-0" />
            <span>Quota tip: Google provides 10,000 quota units every day for free, reset daily at midnight Pacific Time.</span>
          </div>
        </div>
      </section>

      {/* SECTION 2: Google Gemini API */}
      <section id="gemini-api" className="rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] p-6 sm:p-8 space-y-6">
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
              <Sparkles className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-semibold text-[var(--color-ink)]">
                  2. Google Gemini API (Recommended & Free)
                </h2>
                <span className="px-2 py-0.5 rounded text-[11px] bg-blue-500/10 text-blue-400 border border-blue-500/20">
                  15 Requests/Min Free
                </span>
              </div>
              <p className="text-xs text-[var(--color-muted)] mt-0.5">
                Powers AI Studio with viral title generation, SEO descriptions, and high-retention video hooks.
              </p>
            </div>
          </div>

          <a
            href="https://aistudio.google.com/app/apikey"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3.5 py-1.5 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] hover:border-[var(--color-rule-2)] text-xs text-[var(--color-ink)] flex items-center gap-1.5 transition-colors"
          >
            <span>Google AI Studio</span>
            <ExternalLink className="w-3 h-3 text-[var(--color-muted)]" />
          </a>
        </div>

        <div className="space-y-4">
          <h3 className="text-sm font-medium text-[var(--color-ink)]">Step-by-Step Instructions:</h3>
          <ol className="space-y-3.5 text-xs text-[var(--color-muted)] leading-relaxed list-decimal list-inside">
            <li className="pl-1">
              Visit{" "}
              <a
                href="https://aistudio.google.com/app/apikey"
                target="_blank"
                rel="noopener noreferrer"
                className="text-[var(--color-accent)] hover:underline inline-flex items-center gap-0.5"
              >
                Google AI Studio API Keys <ExternalLink className="w-2.5 h-2.5" />
              </a>.
            </li>
            <li className="pl-1">
              Click <strong>&quot;Create API key&quot;</strong> and choose any Google Cloud project.
            </li>
            <li className="pl-1">
              Copy the API Key.
            </li>
            <li className="pl-1">
              Go to{" "}
              <Link href="/settings" className="text-[var(--color-accent)] hover:underline font-medium">
                TubePilot Settings
              </Link>
              , enable <strong>AI Engine</strong>, select <strong>&quot;Google Gemini (Cloud)&quot;</strong>, paste your API key, and select <code>gemini-1.5-flash</code>.
            </li>
            <li className="pl-1">
              Click <strong>&quot;Test Connection&quot;</strong> to confirm it works instantly!
            </li>
          </ol>
        </div>
      </section>

      {/* SECTION 3: Groq Cloud API */}
      <section id="groq-api" className="rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] p-6 sm:p-8 space-y-6">
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
              <Zap className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-semibold text-[var(--color-ink)]">
                  3. Groq Cloud (Ultra-Fast LLaMA 3.3)
                </h2>
                <span className="px-2 py-0.5 rounded text-[11px] bg-amber-500/10 text-amber-400 border border-amber-500/20">
                  Sub-Second Speed
                </span>
              </div>
              <p className="text-xs text-[var(--color-muted)] mt-0.5">
                Groq offers ultra-fast LPUs with free tier limits for models like LLaMA 3.3 70B.
              </p>
            </div>
          </div>

          <a
            href="https://console.groq.com/keys"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3.5 py-1.5 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] hover:border-[var(--color-rule-2)] text-xs text-[var(--color-ink)] flex items-center gap-1.5 transition-colors"
          >
            <span>Groq Console</span>
            <ExternalLink className="w-3 h-3 text-[var(--color-muted)]" />
          </a>
        </div>

        <div className="space-y-4">
          <h3 className="text-sm font-medium text-[var(--color-ink)]">Configuration Values for Groq:</h3>
          <div className="space-y-2 text-xs">
            <div className="flex items-center justify-between p-3 rounded-lg bg-[var(--color-paper-3)] border border-[var(--color-rule)]">
              <div>
                <span className="text-[var(--color-muted)]">Provider Preset: </span>
                <span className="font-mono text-[var(--color-ink)]">Custom OpenAI-Compatible</span>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 rounded-lg bg-[var(--color-paper-3)] border border-[var(--color-rule)]">
              <div>
                <span className="text-[var(--color-muted)]">Base URL: </span>
                <span className="font-mono text-[var(--color-ink)]">https://api.groq.com/openai/v1</span>
              </div>
              <button
                onClick={() => handleCopy("https://api.groq.com/openai/v1", "groq-url")}
                className="text-[var(--color-muted)] hover:text-[var(--color-ink)] flex items-center gap-1"
              >
                {copiedId === "groq-url" ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              </button>
            </div>
            <div className="flex items-center justify-between p-3 rounded-lg bg-[var(--color-paper-3)] border border-[var(--color-rule)]">
              <div>
                <span className="text-[var(--color-muted)]">Model Name: </span>
                <span className="font-mono text-[var(--color-ink)]">llama-3.3-70b-versatile</span>
              </div>
              <button
                onClick={() => handleCopy("llama-3.3-70b-versatile", "groq-model")}
                className="text-[var(--color-muted)] hover:text-[var(--color-ink)] flex items-center gap-1"
              >
                {copiedId === "groq-model" ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 4: Local Offline AI (Ollama & LM Studio) */}
      <section id="local-ai" className="rounded-xl bg-[var(--color-paper-2)] border border-[var(--color-rule)] p-6 sm:p-8 space-y-6">
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
              <Server className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-semibold text-[var(--color-ink)]">
                  4. 100% Free Local AI (Ollama / LM Studio)
                </h2>
                <span className="px-2 py-0.5 rounded text-[11px] bg-purple-500/10 text-purple-400 border border-purple-500/20">
                  Zero Cost • 100% Private
                </span>
              </div>
              <p className="text-xs text-[var(--color-muted)] mt-0.5">
                Run AI completely on your own computer without sending any data to third-party cloud servers.
              </p>
            </div>
          </div>

          <a
            href="https://ollama.com/"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3.5 py-1.5 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] hover:border-[var(--color-rule-2)] text-xs text-[var(--color-ink)] flex items-center gap-1.5 transition-colors"
          >
            <span>Ollama Website</span>
            <ExternalLink className="w-3 h-3 text-[var(--color-muted)]" />
          </a>
        </div>

        <div className="space-y-4">
          <h3 className="text-sm font-medium text-[var(--color-ink)]">Quick Setup for Ollama:</h3>
          <div className="space-y-3">
            <div className="p-3.5 rounded-lg bg-black/40 border border-[var(--color-rule)] font-mono text-xs text-emerald-400 flex items-center justify-between">
              <span>ollama run qwen2.5:3b</span>
              <button
                onClick={() => handleCopy("ollama run qwen2.5:3b", "ollama-cmd")}
                className="text-[var(--color-muted)] hover:text-white"
              >
                {copiedId === "ollama-cmd" ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
              </button>
            </div>
            <p className="text-xs text-[var(--color-muted)] leading-relaxed">
              Once Ollama is running on your machine, go to{" "}
              <Link href="/settings" className="text-[var(--color-accent)] hover:underline font-medium">
                Settings
              </Link>
              , choose <strong>&quot;Ollama (Local)&quot;</strong>, set Base URL to <code>http://127.0.0.1:11434</code>, and click Save.
            </p>
          </div>
        </div>
      </section>

      {/* Bottom CTA Card */}
      <div className="p-8 rounded-xl bg-gradient-to-r from-[var(--color-paper-2)] to-[var(--color-paper-3)] border border-[var(--color-rule-2)] flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="space-y-1.5 text-center sm:text-left">
          <h3 className="text-lg font-semibold text-[var(--color-ink)]">Ready to configure your keys?</h3>
          <p className="text-xs text-[var(--color-muted)] max-w-lg">
            All API keys are securely stored only in your local instance and never transmitted to any external analytics.
          </p>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          <Link
            href="/settings"
            className="px-6 py-3 rounded-lg bg-[var(--color-accent)] hover:bg-[var(--color-accent)]/90 text-[var(--color-accent-ink)] font-medium text-sm flex items-center gap-2 shadow-sm transition-all"
          >
            <span>Go to Settings</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  );
}
