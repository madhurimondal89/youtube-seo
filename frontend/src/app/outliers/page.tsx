"use client";

import React, { useState, useEffect } from "react";
import { TrendingUp, Zap, ExternalLink, Play, Sparkles } from "lucide-react";
import { getOutliers } from "@/lib/api";
import { OutlierVideoItem } from "@/lib/types";
import DataProvenanceBadge from "@/components/common/DataProvenanceBadge";

export default function OutliersPage() {
  const [channel, setChannel] = useState("@creatoracademy");
  const [outliers, setOutliers] = useState<OutlierVideoItem[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchOutliers = async (chan: string) => {
    setLoading(true);
    try {
      const res = await getOutliers(chan);
      setOutliers(res);
    } catch {
      // Graceful fallback
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOutliers(channel);
  }, []);

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Statistical Outlier Detector</h1>
          <p className="text-xs sm:text-sm text-slate-400">
            Identify breakout videos performing 3x to 30x above their channel&apos;s baseline using Median &amp; MAD statistics.
          </p>
        </div>
      </div>

      {/* Input */}
      <div className="glass-panel p-5">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            fetchOutliers(channel);
          }}
          className="flex flex-col sm:flex-row gap-3"
        >
          <input
            type="text"
            value={channel}
            onChange={(e) => setChannel(e.target.value)}
            placeholder="Enter channel handle (e.g. '@hubspot', '@creatoracademy')..."
            className="flex-1 bg-slate-900/90 border border-slate-700/80 rounded-lg px-4 py-2.5 text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:border-indigo-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm flex items-center justify-center gap-2"
          >
            <Zap className="w-4 h-4" />
            <span>{loading ? "Scanning..." : "Detect Outliers"}</span>
          </button>
        </form>
      </div>

      {/* Outlier Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {outliers.map((item, idx) => (
          <div key={idx} className="glass-card p-5 rounded-xl space-y-4 border border-slate-800 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span
                  className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                    item.tier === "Viral Outlier"
                      ? "bg-rose-500/10 text-rose-400 border-rose-500/30"
                      : item.tier === "High Outlier"
                      ? "bg-indigo-500/10 text-indigo-400 border-indigo-500/30"
                      : "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
                  }`}
                >
                  {item.tier}
                </span>
                <span className="text-xs font-bold text-cyan-400 bg-cyan-950/40 px-2 py-0.5 rounded border border-cyan-800/40">
                  {item.multiplier_text}
                </span>
              </div>

              <h3 className="text-sm font-bold text-white line-clamp-2">{item.title}</h3>
              <p className="text-xs text-slate-400">{item.channel_name}</p>
            </div>

            <div className="pt-3 border-t border-slate-800/80 space-y-2 text-xs">
              <div className="flex justify-between text-slate-400">
                <span>Video Views:</span>
                <span className="font-bold text-slate-100">{item.views.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Channel Baseline Median:</span>
                <span className="font-medium text-slate-300">{item.channel_median_views.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Robust Z-Score:</span>
                <span className="font-mono text-indigo-400">+{item.z_score}σ</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
