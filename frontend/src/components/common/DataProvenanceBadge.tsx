"use client";

import React from "react";
import { DataProvenance } from "@/lib/types";

interface Props {
  provenance: DataProvenance;
  showTooltip?: boolean;
}

export default function DataProvenanceBadge({ provenance }: Props) {
  const configs: Record<DataProvenance, { label: string; bg: string; text: string; border: string }> = {
    Official: {
      label: "Official API",
      bg: "bg-blue-500/10",
      text: "text-blue-400",
      border: "border-blue-500/25",
    },
    Public: {
      label: "Public Web",
      bg: "bg-emerald-500/10",
      text: "text-emerald-400",
      border: "border-emerald-500/25",
    },
    Calculated: {
      label: "Calculated",
      bg: "bg-purple-500/10",
      text: "text-purple-400",
      border: "border-purple-500/25",
    },
    Estimated: {
      label: "Estimated Signal",
      bg: "bg-cyan-500/10",
      text: "text-cyan-400",
      border: "border-cyan-500/25",
    },
    Relative: {
      label: "Relative Index",
      bg: "bg-amber-500/10",
      text: "text-amber-400",
      border: "border-amber-500/25",
    },
    "Sample Data": {
      label: "Sample Demo Data",
      bg: "bg-orange-500/10",
      text: "text-orange-400",
      border: "border-orange-500/25",
    },
    "AI Recommendation": {
      label: "AI Recommendation",
      bg: "bg-pink-500/10",
      text: "text-pink-400",
      border: "border-pink-500/25",
    },
    Unavailable: {
      label: "Unavailable",
      bg: "bg-slate-500/10",
      text: "text-slate-400",
      border: "border-slate-500/25",
    },
  };

  const conf = configs[provenance] || configs.Calculated;

  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${conf.bg} ${conf.text} ${conf.border}`}
      title={`Data Provenance: ${provenance}. Never fabricated.`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current mr-1.5 opacity-80" />
      {conf.label}
    </span>
  );
}
