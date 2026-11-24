"use client";

import React, { useState } from "react";
import {
  Monitor,
  Smartphone,
  CheckCircle2,
  Image as ImageIcon,
  Clock,
  Eye,
  Subtitles,
  AlertTriangle,
  Layers,
} from "lucide-react";

interface SerpThumbnailPreviewProps {
  title: string;
  description?: string;
  channelName?: string;
  viewsText?: string;
  publishedTimeText?: string;
  durationText?: string;
  thumbnailUrl?: string;
  hasChapters?: boolean;
  hasCaptions?: boolean;
  onThumbnailChange?: (url: string) => void;
}

export default function SerpThumbnailPreview({
  title,
  description = "Detailed walkthrough with step-by-step techniques and practical optimization tips...",
  channelName = "Your Channel Name",
  viewsText = "125K views",
  publishedTimeText = "3 days ago",
  durationText = "14:20",
  thumbnailUrl,
  hasChapters = false,
  hasCaptions = false,
  onThumbnailChange,
}: SerpThumbnailPreviewProps) {
  const [deviceMode, setDeviceMode] = useState<"desktop" | "mobile">("desktop");
  const [customThumb, setCustomThumb] = useState(thumbnailUrl || "");

  const displayTitle = title.trim() || "Your Compelling Video Title Goes Here";
  const displayThumb = customThumb || thumbnailUrl;
  const titleCharCount = displayTitle.length;

  // Mobile truncates at around 48-52 chars, desktop shows up to ~70-80 chars before ...
  const isMobileTruncated = displayTitle.length > 52;
  const isDesktopTruncated = displayTitle.length > 72;

  let lengthBadgeColor = "text-emerald-400 bg-emerald-500/10 border-emerald-500/30";
  if (titleCharCount > 70 || titleCharCount < 40) {
    lengthBadgeColor = "text-amber-400 bg-amber-500/10 border-amber-500/30";
  }
  if (titleCharCount > 85 || titleCharCount < 25) {
    lengthBadgeColor = "text-rose-400 bg-rose-500/10 border-rose-500/30";
  }

  const handleThumbInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCustomThumb(e.target.value);
    if (onThumbnailChange) {
      onThumbnailChange(e.target.value);
    }
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur-sm space-y-4 shadow-xl">
      {/* Header with Mode Toggle & Stats */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <ImageIcon className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">SERP & Thumbnail Preview</h3>
            <p className="text-xs text-slate-400">See how your video appears in real YouTube search feeds</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className={`px-2.5 py-1 rounded-full text-xs font-medium border flex items-center gap-1.5 ${lengthBadgeColor}`}>
            <span>{titleCharCount}/70 chars</span>
            {titleCharCount > 70 && <AlertTriangle className="w-3 h-3 text-amber-400" />}
          </div>

          <div className="inline-flex rounded-lg bg-slate-800/80 p-0.5 border border-slate-700/60">
            <button
              type="button"
              onClick={() => setDeviceMode("desktop")}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-medium transition-all ${
                deviceMode === "desktop"
                  ? "bg-indigo-600 text-white shadow"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Monitor className="w-3.5 h-3.5" />
              <span>Desktop SERP</span>
            </button>
            <button
              type="button"
              onClick={() => setDeviceMode("mobile")}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-medium transition-all ${
                deviceMode === "mobile"
                  ? "bg-indigo-600 text-white shadow"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Smartphone className="w-3.5 h-3.5" />
              <span>Mobile Feed</span>
            </button>
          </div>
        </div>
      </div>

      {/* Simulator Container Styled like YouTube Dark Theme */}
      <div className="p-4 sm:p-6 rounded-xl bg-[#0f0f0f] border border-slate-800/90 shadow-2xl overflow-hidden">
        {deviceMode === "desktop" ? (
          /* DESKTOP SEARCH RESULT CARD */
          <div className="flex flex-col sm:flex-row gap-4 max-w-4xl items-start">
            {/* Thumbnail 16:9 */}
            <div className="relative w-full sm:w-80 aspect-video rounded-xl overflow-hidden bg-slate-800 flex-shrink-0 group border border-slate-800">
              {displayThumb ? (
                <img
                  src={displayThumb}
                  alt={displayTitle}
                  className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                  onError={() => setCustomThumb("")}
                />
              ) : (
                <div className="w-full h-full flex flex-col items-center justify-center text-slate-500 p-4 text-center bg-gradient-to-br from-slate-900 to-slate-800">
                  <ImageIcon className="w-8 h-8 mb-2 text-slate-600" />
                  <span className="text-xs font-medium text-slate-400">16:9 Thumbnail</span>
                  <span className="text-[10px] text-slate-500 mt-1">1280 × 720 px recommended</span>
                </div>
              )}
              {/* Duration badge */}
              <div className="absolute bottom-2 right-2 px-1.5 py-0.5 rounded bg-black/80 text-[11px] font-medium text-white flex items-center gap-1">
                <span>{durationText}</span>
              </div>
            </div>

            {/* Video Meta in Search */}
            <div className="flex-1 space-y-2 min-w-0">
              <h4 className="text-base sm:text-lg font-normal text-white line-clamp-2 leading-snug hover:text-indigo-300 transition-colors cursor-pointer">
                {displayTitle}
              </h4>
              <div className="flex items-center gap-2 text-xs text-[#aaaaaa]">
                <span>{viewsText}</span>
                <span>•</span>
                <span>{publishedTimeText}</span>
              </div>

              {/* Channel Row */}
              <div className="flex items-center gap-2 pt-1 pb-1">
                <div className="w-6 h-6 rounded-full bg-indigo-600 flex items-center justify-center text-[10px] font-bold text-white uppercase flex-shrink-0">
                  {channelName.charAt(0)}
                </div>
                <span className="text-xs text-[#aaaaaa] font-medium flex items-center gap-1">
                  {channelName}
                  <CheckCircle2 className="w-3.5 h-3.5 text-slate-400 fill-slate-400 text-black" />
                </span>
              </div>

              {/* Description Snippet */}
              <p className="text-xs text-[#aaaaaa] line-clamp-2 leading-relaxed">
                {description || "No description provided."}
              </p>

              {/* Feature Badges */}
              <div className="flex flex-wrap items-center gap-1.5 pt-1">
                <span className="px-1.5 py-0.5 rounded bg-[#272727] text-[10px] font-semibold text-[#f1f1f1]">
                  4K
                </span>
                {hasCaptions && (
                  <span className="px-1.5 py-0.5 rounded bg-[#272727] text-[10px] font-semibold text-emerald-300 flex items-center gap-0.5">
                    <Subtitles className="w-3 h-3" /> CC
                  </span>
                )}
                {hasChapters && (
                  <span className="px-1.5 py-0.5 rounded bg-[#272727] text-[10px] font-semibold text-indigo-300 flex items-center gap-0.5">
                    <Layers className="w-3 h-3" /> Chapters
                  </span>
                )}
              </div>
            </div>
          </div>
        ) : (
          /* MOBILE FEED CARD */
          <div className="max-w-sm mx-auto space-y-3">
            {/* Full-width 16:9 Thumbnail */}
            <div className="relative w-full aspect-video rounded-xl overflow-hidden bg-slate-800 border border-slate-800">
              {displayThumb ? (
                <img
                  src={displayThumb}
                  alt={displayTitle}
                  className="w-full h-full object-cover"
                  onError={() => setCustomThumb("")}
                />
              ) : (
                <div className="w-full h-full flex flex-col items-center justify-center text-slate-500 p-4 text-center bg-gradient-to-br from-slate-900 to-slate-800">
                  <ImageIcon className="w-8 h-8 mb-2 text-slate-600" />
                  <span className="text-xs font-medium text-slate-400">Mobile Feed Preview</span>
                </div>
              )}
              <div className="absolute bottom-2 right-2 px-1.5 py-0.5 rounded bg-black/85 text-[10px] font-medium text-white">
                {durationText}
              </div>
            </div>

            {/* Mobile Title & Channel Row */}
            <div className="flex gap-3 items-start px-1">
              <div className="w-9 h-9 rounded-full bg-indigo-600 flex items-center justify-center text-xs font-bold text-white uppercase flex-shrink-0">
                {channelName.charAt(0)}
              </div>
              <div className="flex-1 min-w-0 space-y-1">
                <h4 className="text-sm font-medium text-white line-clamp-2 leading-snug">
                  {displayTitle}
                </h4>
                <div className="flex items-center gap-1.5 text-[11px] text-[#aaaaaa]">
                  <span className="truncate max-w-[120px]">{channelName}</span>
                  <span>•</span>
                  <span>{viewsText}</span>
                  <span>•</span>
                  <span>{publishedTimeText}</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Truncation & Optimization Feedback */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
        <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-800 text-xs space-y-1">
          <div className="font-medium text-slate-300 flex items-center gap-1.5">
            <Monitor className="w-3.5 h-3.5 text-indigo-400" />
            <span>Desktop Title Display</span>
          </div>
          <p className="text-slate-400">
            {isDesktopTruncated ? (
              <span className="text-amber-400">
                Title will truncate after ~70 characters on standard desktop search viewports.
              </span>
            ) : (
              <span className="text-emerald-400">
                Title fits completely on desktop without awkward truncation.
              </span>
            )}
          </p>
        </div>

        <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-800 text-xs space-y-1">
          <div className="font-medium text-slate-300 flex items-center gap-1.5">
            <Smartphone className="w-3.5 h-3.5 text-cyan-400" />
            <span>Mobile Title Display</span>
          </div>
          <p className="text-slate-400">
            {isMobileTruncated ? (
              <span className="text-amber-400">
                Second line cuts off after ~50 characters on mobile screens. Front-load your main hook!
              </span>
            ) : (
              <span className="text-emerald-400">
                Title is concise and visible in full across mobile search and suggested feeds.
              </span>
            )}
          </p>
        </div>
      </div>

      {/* Custom Thumbnail Input */}
      <div className="flex items-center gap-2 pt-2">
        <input
          type="text"
          value={customThumb}
          onChange={handleThumbInput}
          placeholder="Paste custom thumbnail image URL (e.g. https://...)..."
          className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
        />
        {customThumb && (
          <button
            type="button"
            onClick={() => setCustomThumb("")}
            className="text-xs text-slate-400 hover:text-white px-2 py-2"
          >
            Clear
          </button>
        )}
      </div>
    </div>
  );
}
