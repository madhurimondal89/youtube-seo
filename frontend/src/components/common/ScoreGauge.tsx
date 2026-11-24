"use client";

import React from "react";

interface Props {
  score: number;
  size?: "sm" | "md" | "lg";
  label?: string;
  sublabel?: string;
}

export default function ScoreGauge({ score, size = "md", label, sublabel }: Props) {
  const bounded = Math.max(0, Math.min(100, Math.round(score)));

  let strokeColor = "#10b981"; // emerald
  let textColor = "text-emerald-400";
  if (bounded < 45) {
    strokeColor = "#f43f5e"; // rose
    textColor = "text-rose-400";
  } else if (bounded < 70) {
    strokeColor = "#f59e0b"; // amber
    textColor = "text-amber-400";
  } else if (bounded < 85) {
    strokeColor = "#06b6d4"; // cyan
    textColor = "text-cyan-400";
  }

  const dim = size === "sm" ? 48 : size === "lg" ? 110 : 76;
  const strokeWidth = size === "sm" ? 4 : size === "lg" ? 8 : 6;
  const radius = (dim - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (bounded / 100) * circumference;

  return (
    <div className="flex items-center gap-3">
      <div className="relative inline-flex items-center justify-center" style={{ width: dim, height: dim }}>
        <svg width={dim} height={dim} className="transform -rotate-90">
          <circle
            cx={dim / 2}
            cy={dim / 2}
            r={radius}
            stroke="rgba(255, 255, 255, 0.08)"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          <circle
            cx={dim / 2}
            cy={dim / 2}
            r={radius}
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-700 ease-out"
          />
        </svg>
        <span
          className={`absolute font-bold tracking-tight ${textColor} ${
            size === "sm" ? "text-xs" : size === "lg" ? "text-2xl" : "text-base"
          }`}
        >
          {bounded}
        </span>
      </div>
      {(label || sublabel) && (
        <div className="flex flex-col">
          {label && <span className="text-sm font-semibold text-slate-200">{label}</span>}
          {sublabel && <span className="text-xs text-slate-400">{sublabel}</span>}
        </div>
      )}
    </div>
  );
}
