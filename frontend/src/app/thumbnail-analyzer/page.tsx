"use client";

import React, { useState } from "react";
import {
  Upload,
  Image as ImageIcon,
  AlertTriangle,
  CheckCircle,
  Smartphone,
  Monitor,
  Sparkles,
  Info,
  Layers,
  ArrowRight,
} from "lucide-react";
import ScoreGauge from "@/components/common/ScoreGauge";
import SerpThumbnailPreview from "@/components/common/SerpThumbnailPreview";
import { analyzeThumbnailUpload, analyzeThumbnailUrl } from "@/lib/api";
import { ThumbnailAnalysisResponse } from "@/lib/types";

export default function ThumbnailAnalyzerPage() {
  const [imageUrl, setImageUrl] = useState("");
  const [previewSrc, setPreviewSrc] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ThumbnailAnalysisResponse | null>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setError(null);
    setLoading(true);

    // Create object URL for local preview
    const objectUrl = URL.createObjectURL(file);
    setPreviewSrc(objectUrl);

    try {
      const res = await analyzeThumbnailUpload(file);
      setResult(res);
    } catch (err: any) {
      setError(err.message || "Failed to analyze thumbnail upload");
    } finally {
      setLoading(false);
    }
  };

  const handleUrlSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!imageUrl.trim()) return;

    setError(null);
    setLoading(true);
    setPreviewSrc(imageUrl.trim());

    try {
      const res = await analyzeThumbnailUrl(imageUrl.trim());
      setResult(res);
    } catch (err: any) {
      setError(err.message || "Failed to analyze thumbnail from URL");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-[1500px] mx-auto space-y-6">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-2xl font-medium tracking-tight text-[var(--color-ink)]">
          Thumbnail Vision &amp; Mobile Readability Analysis
        </h1>
        <p className="text-xs text-[var(--color-muted)]">
          Deterministic luminance, contrast distribution, safety zones, and simulated SERP legibility for high-CTR thumbnails.
        </p>
      </div>

      {/* Input Methods: Drag & Drop / URL */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Upload Box */}
        <div className="panel-console p-6 flex flex-col justify-center items-center text-center border-dashed border-2 border-[var(--color-rule-2)] rounded-xl relative">
          <input
            type="file"
            accept="image/png, image/jpeg, image/webp"
            onChange={handleFileUpload}
            className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
            title="Upload thumbnail image"
          />
          <div className="w-12 h-12 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] flex items-center justify-center text-[var(--color-accent)] mb-3">
            <Upload className="w-6 h-6" />
          </div>
          <span className="text-sm font-medium text-[var(--color-ink)]">
            Click or drag &amp; drop thumbnail here
          </span>
          <span className="text-xs text-[var(--color-muted)] mt-1">
            Supports PNG, JPG, or WebP up to 10MB (1280x720 recommended)
          </span>
        </div>

        {/* URL Box */}
        <div className="panel-console p-6 flex flex-col justify-between">
          <div className="space-y-1 mb-4">
            <span className="text-sm font-medium text-[var(--color-ink)]">
              Or analyze via public image / video URL
            </span>
            <p className="text-xs text-[var(--color-muted)]">
              Paste direct image link or YouTube thumbnail CDN URL.
            </p>
          </div>

          <form onSubmit={handleUrlSubmit} className="flex gap-2">
            <input
              type="url"
              value={imageUrl}
              onChange={(e) => setImageUrl(e.target.value)}
              placeholder="https://i.ytimg.com/vi/.../maxresdefault.jpg"
              className="flex-1 bg-[var(--color-paper-3)] border border-[var(--color-rule)] rounded-md px-3 py-2 text-xs text-[var(--color-ink)] placeholder-[var(--color-muted)] focus:outline-none focus:border-[var(--color-rule-2)]"
            />
            <button
              type="submit"
              disabled={loading || !imageUrl.trim()}
              className="px-4 py-2 rounded-md bg-[var(--color-accent)] hover:bg-[var(--color-accent)]/90 text-[var(--color-accent-ink)] font-medium text-xs disabled:opacity-50"
            >
              {loading ? "Analyzing..." : "Analyze URL"}
            </button>
          </form>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-md bg-[var(--color-bad-soft)] border border-[var(--color-bad)]/40 text-xs text-[var(--color-bad)]">
          {error}
        </div>
      )}

      {/* Results View */}
      {result && (
        <div className="space-y-6">
          {/* Top Score Banner */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="panel-console p-5 flex items-center justify-between">
              <div className="space-y-1">
                <span className="text-xs text-[var(--color-muted)]">Overall Vision Score</span>
                <div className="text-3xl font-normal text-[var(--color-ink)] measured">
                  {result.overall_score}<span className="text-xs text-[var(--color-muted)]">/100</span>
                </div>
                <span className="text-[11px] text-[var(--color-muted)]">
                  {result.is_standard_hd ? "HD 16:9 Standard" : "Non-Standard Framing"}
                </span>
              </div>
              <ScoreGauge score={result.overall_score} size="md" />
            </div>

            <div className="panel-console p-5 space-y-1">
              <span className="text-xs text-[var(--color-muted)]">Aspect Ratio</span>
              <div className="text-xl font-normal text-[var(--color-cool)] measured">
                {result.aspect_ratio_label}
              </div>
              <span className="text-[11px] text-[var(--color-muted)]">
                Resolution: {result.width} x {result.height} px
              </span>
            </div>

            <div className="panel-console p-5 space-y-1">
              <span className="text-xs text-[var(--color-muted)]">Luminance &amp; Contrast</span>
              <div className="text-xl font-normal text-[var(--color-accent)] measured">
                {result.contrast_ratio}x Ratio
              </div>
              <span className="text-[11px] text-[var(--color-muted)]">
                Brightness: {result.average_brightness}/255
              </span>
            </div>

            <div className="panel-console p-5 space-y-1">
              <span className="text-xs text-[var(--color-muted)]">Mobile Safe Zone</span>
              <div className="text-xs font-medium text-[var(--color-ink)] pt-1">
                {result.breakdown.mobile_readability_score >= 70 ? (
                  <span className="text-[var(--color-ok)] flex items-center gap-1">
                    <CheckCircle className="w-4 h-4" /> Legible at small scale
                  </span>
                ) : (
                  <span className="text-[var(--color-bad)] flex items-center gap-1">
                    <AlertTriangle className="w-4 h-4" /> Risk of blur at mobile size
                  </span>
                )}
              </div>
              <p className="text-[11px] text-[var(--color-muted)] leading-tight pt-1">
                {result.mobile_preview_advisory}
              </p>
            </div>
          </div>

          {/* Breakdown & SERP Simulator */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Visual Simulator */}
            <div className="panel-console p-6 space-y-4">
              <div className="flex items-center justify-between border-b border-[var(--color-rule)] pb-3">
                <span className="text-sm font-medium text-[var(--color-ink)]">
                  Live SERP Simulation Preview
                </span>
                <span className="text-xs text-[var(--color-muted)]">
                  Timestamp Safe Zone Verification
                </span>
              </div>

              <SerpThumbnailPreview
                thumbnailUrl={previewSrc || undefined}
                title="High-CTR YouTube Title Shown Here in Preview Format"
                channelName="Creator Channel"
              />

              {/* Dominant Palette */}
              {result.dominant_colors.length > 0 && (
                <div className="pt-2">
                  <span className="text-xs text-[var(--color-muted)] block mb-2">
                    Dominant Thumbnail Palette:
                  </span>
                  <div className="flex gap-2">
                    {result.dominant_colors.map((c, idx) => (
                      <div
                        key={idx}
                        className="flex items-center gap-1.5 px-2 py-1 rounded bg-[var(--color-paper-3)] border border-[var(--color-rule)] text-[11px] measured"
                      >
                        <span
                          className="w-3.5 h-3.5 rounded-sm border border-white/20"
                          style={{ backgroundColor: c }}
                        />
                        <span className="text-[var(--color-muted)]">{c}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Issues & Checklist */}
            <div className="panel-console p-6 space-y-4">
              <div className="flex items-center justify-between border-b border-[var(--color-rule)] pb-3">
                <span className="text-sm font-medium text-[var(--color-ink)]">
                  Visual Diagnostics &amp; Issues ({result.issues.length})
                </span>
                <span className="text-xs text-[var(--color-muted)]">
                  Provenance: {result.data_provenance}
                </span>
              </div>

              {result.issues.length === 0 ? (
                <div className="p-4 rounded-md bg-[var(--color-ok-soft)] border border-[var(--color-rule)] text-xs text-[var(--color-ok)]">
                  Zero critical visual flaws detected. Thumbnail complies with 16:9 framing, contrast standards, and mobile safety zones.
                </div>
              ) : (
                <div className="space-y-2.5 max-h-[380px] overflow-y-auto pr-1">
                  {result.issues.map((issue, idx) => (
                    <div
                      key={idx}
                      className="p-3 rounded-md bg-[var(--color-paper-3)] border border-[var(--color-rule)] space-y-1"
                    >
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-medium text-[var(--color-ink)]">{issue.category}</span>
                        <span
                          className={`px-1.5 py-0.5 rounded text-[10px] ${
                            issue.severity === "critical"
                              ? "bg-[var(--color-bad-soft)] text-[var(--color-bad)] border border-[var(--color-bad)]/40"
                              : "bg-[var(--color-paper-2)] text-[var(--color-muted)]"
                          }`}
                        >
                          {issue.severity}
                        </span>
                      </div>
                      <p className="text-xs text-[var(--color-muted)]">{issue.issue}</p>
                      <p className="text-xs text-[var(--color-accent)] leading-relaxed">
                        Suggestion: {issue.suggestion}
                      </p>
                    </div>
                  ))}
                </div>
              )}

              {/* Recommendations */}
              <div className="border-t border-[var(--color-rule)] pt-3 space-y-2">
                <span className="text-xs font-medium text-[var(--color-ink)]">
                  Optimization Recommendations
                </span>
                <ul className="space-y-1.5 text-xs text-[var(--color-muted)] list-disc pl-4">
                  {result.recommendations.map((rec, i) => (
                    <li key={i}>{rec}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
