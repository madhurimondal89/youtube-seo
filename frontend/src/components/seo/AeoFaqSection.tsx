"use client";

import React, { useState } from "react";
import { HelpCircle, ChevronDown, Sparkles, CheckCircle2 } from "lucide-react";

interface FaqItem {
  question: string;
  shortAnswer: string;
  detailedAnswer: string;
}

const FAQ_ITEMS: FaqItem[] = [
  {
    question: "How is TubePilot AI different from vidIQ and TubeBuddy?",
    shortAnswer:
      "TubePilot AI is an independent, self-hosted YouTube SEO platform that calculates scores using transparent mathematical statistics instead of proprietary, opaque algorithms or mandatory paid AI subscriptions.",
    detailedAnswer:
      "Unlike vidIQ and TubeBuddy which lock essential keyword tools behind tiered monthly subscriptions and opaque proprietary scores, TubePilot AI runs completely transparently. Every Opportunity Score, Competition Index, and Outlier Multiplier is grounded in deterministic statistical formulas (like Median Absolute Deviation). It can operate 100% offline or with zero-cost public data without forced paid API tokens.",
  },
  {
    question: "How is the YouTube Keyword Opportunity Score calculated?",
    shortAnswer:
      "The Opportunity Score (0-100) combines 10 mathematical signals: Relative Demand Index (RDI), Estimated Competition, Long-Tail Specificity, Search Intent, Velocity Momentum, Title Match Exactness, Saturation Penalty, Channel Diversity, Video Freshness, and Top-10 Dispersion.",
    detailedAnswer:
      "LLMs never hallucinate numerical scores in TubePilot. When you research a seed keyword, the system gathers public autocomplete rankings and the top 15 SERP competitors. It weighs high search demand against low creator competition while giving multiplier bonuses for actionable search intents like tutorials, how-to guides, and commercial comparison queries.",
  },
  {
    question: "What checks are included in the 18-point Video SEO Audit?",
    shortAnswer:
      "The 18-point audit evaluates Title length (50-70 chars), keyword positioning in the first 3 words, 200+ word descriptions with chapter timestamps, targeted long-tail tags, 16:9 thumbnail contrast, and engagement triggers.",
    detailedAnswer:
      "The audit inspects 6 core categories: Title Optimization (20%), Description Quality (20%), Keyword Alignment (20%), Tag Strategy (15%), Engagement & Retention Features (15%), and Metadata Quality (10%). It automatically identifies missing chapter timestamps (which enable Google Key Moments), weak opening hooks, and tag-to-title keyword disconnects.",
  },
  {
    question: "How does Outlier Detection identify viral YouTube topics?",
    shortAnswer:
      "TubePilot AI calculates the channel's 30-video median view count and compares each video against this baseline using Median Absolute Deviation (MAD). Videos performing at 3x to 30x the median are isolated as true viral outliers.",
    detailedAnswer:
      "Standard averages fail because a single million-view video distorts the mean. By utilizing median statistics, TubePilot reliably reveals topics, titles, and thumbnails that caused smaller channels to break out of their normal subscriber reach. Creators can model these proven outlier angles for their own niche.",
  },
  {
    question: "Does TubePilot AI require paid YouTube or OpenAI API keys?",
    shortAnswer:
      "No. TubePilot AI operates out-of-the-box using ethical public autocomplete and video SERP extraction, alongside a deterministic heuristic creator studio that works 100% offline without any paid API keys.",
    detailedAnswer:
      "Paid keys are entirely optional. If you desire official Google quota, you can plug in a free YouTube Data API v3 key. If you desire cloud AI, you can connect OpenAI or Gemini keys, or connect a local free Ollama model (Qwen 2.5) on your CPU with zero subscription cost.",
  },
  {
    question: "Is TubePilot safe and compliant with YouTube Terms of Service?",
    shortAnswer:
      "Yes. TubePilot AI accesses only publicly available metadata using rate-paced queries with randomized jitter and respectful timeouts, never bypassing CAPTCHAs, bot challenges, or user login protections.",
    detailedAnswer:
      "Data collection follows strict lawful and ethical practices. The platform caches all requests for 15 minutes (900 seconds) to avoid redundant requests, rate-limits queries to under 60 per minute, and halts immediately if any security challenge is detected.",
  },
];

export default function AeoFaqSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  // Structured Data (JSON-LD) for Google FAQPage & AI Answer Engines
  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: FAQ_ITEMS.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: {
        "@type": "Answer",
        text: `${item.shortAnswer} ${item.detailedAnswer}`,
      },
    })),
  };

  return (
    <section className="mt-12 space-y-6" aria-labelledby="aeo-faq-heading">
      {/* Inject FAQPage Structured Data for Google AEO */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      />

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[var(--color-rule)] pb-4">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-2 text-xs font-semibold tracking-wider uppercase text-[var(--color-accent)]">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Answer Engine Optimization & Knowledge Base</span>
          </div>
          <h2 id="aeo-faq-heading" className="text-xl font-bold tracking-tight text-[var(--color-ink)]">
            Frequently Asked Questions & Methodology
          </h2>
        </div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-[var(--color-paper-2)] border border-[var(--color-rule)] text-[var(--color-muted)]">
          <CheckCircle2 className="w-3.5 h-3.5 text-[var(--color-ok)]" />
          <span>Google AI Overview & FAQ Schema Ready</span>
        </div>
      </div>

      <div className="space-y-3">
        {FAQ_ITEMS.map((item, idx) => {
          const isOpen = openIndex === idx;
          return (
            <div
              key={idx}
              className="rounded-xl border border-[var(--color-rule)] bg-[var(--color-paper-2)] overflow-hidden transition-all duration-200"
            >
              <button
                type="button"
                onClick={() => setOpenIndex(isOpen ? null : idx)}
                className="w-full p-4 sm:p-5 text-left flex items-start justify-between gap-4 hover:bg-[var(--color-paper-3)] transition-colors"
                aria-expanded={isOpen}
              >
                <div className="flex items-start gap-3">
                  <div className="mt-0.5 w-6 h-6 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center shrink-0 text-[var(--color-accent)] font-mono text-xs font-bold">
                    Q{idx + 1}
                  </div>
                  <span className="text-sm sm:text-base font-semibold text-[var(--color-ink)]">
                    {item.question}
                  </span>
                </div>
                <ChevronDown
                  className={`w-4 h-4 mt-1 text-[var(--color-muted)] shrink-0 transition-transform duration-200 ${
                    isOpen ? "rotate-180 text-[var(--color-accent)]" : ""
                  }`}
                />
              </button>

              {isOpen && (
                <div className="px-5 pb-5 pt-1 space-y-3 border-t border-[var(--color-rule)] bg-[var(--color-paper-1)]">
                  {/* Direct Answer Paragraph for Featured Snippets / AI Overviews */}
                  <div className="p-3.5 rounded-lg bg-[var(--color-paper-2)] border-l-4 border-l-[var(--color-accent)] text-xs sm:text-sm text-[var(--color-ink)] leading-relaxed font-medium">
                    <span className="font-bold text-[var(--color-accent)] block mb-1">Direct Answer:</span>
                    {item.shortAnswer}
                  </div>
                  <p className="text-xs sm:text-sm text-[var(--color-muted)] leading-relaxed">
                    {item.detailedAnswer}
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
