"use client";

import React, { useState, useEffect } from "react";
import { Compass, Sparkles, FolderTree, ListVideo, Layers, ArrowRight } from "lucide-react";
import { researchKeyword } from "@/lib/api";
import { TopicCluster } from "@/lib/types";
import ScoreGauge from "@/components/common/ScoreGauge";
import Link from "next/link";

export default function TopicsPage() {
  const [topic, setTopic] = useState("AI Video Generation");
  const [clusters, setClusters] = useState<TopicCluster[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchClusters = async (t: string) => {
    setLoading(true);
    try {
      const res = await researchKeyword(t, true, true, 30);
      setClusters(res.clusters);
    } catch {
      // Graceful fallback
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClusters(topic);
  }, []);

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Topic Explorer & Clusters</h1>
          <p className="text-xs sm:text-sm text-slate-400">
            Pillar-and-cluster content mapping to build topical authority without creating disconnected videos.
          </p>
        </div>
      </div>

      {/* Input */}
      <div className="glass-panel p-5">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            fetchClusters(topic);
          }}
          className="flex flex-col sm:flex-row gap-3"
        >
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter high-level niche (e.g. 'AI Video Generation', 'Personal Finance')..."
            className="flex-1 bg-slate-900/90 border border-slate-700/80 rounded-lg px-4 py-2.5 text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:border-indigo-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm flex items-center justify-center gap-2"
          >
            <Compass className="w-4 h-4" />
            <span>{loading ? "Clustering..." : "Build Clusters"}</span>
          </button>
        </form>
      </div>

      {/* Clusters Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {clusters.map((cluster, i) => (
          <div key={i} className="glass-card p-6 rounded-xl space-y-4 border border-slate-800">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-[10px] text-cyan-400 font-bold uppercase tracking-wider">
                  Topical Authority Cluster
                </span>
                <h3 className="text-lg font-bold text-white mt-0.5">{cluster.cluster_name}</h3>
              </div>
              <ScoreGauge score={cluster.avg_opportunity_score} size="sm" />
            </div>

            {/* Pillar Video */}
            <div className="p-3.5 rounded-lg bg-slate-900/80 border border-slate-800 space-y-1">
              <span className="text-[10px] text-indigo-400 font-semibold uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles className="w-3 h-3" /> Recommended Pillar Hero Video
              </span>
              <p className="text-sm font-bold text-slate-100">{cluster.recommended_pillar_title}</p>
            </div>

            {/* Supporting Videos */}
            <div className="space-y-2">
              <span className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                <ListVideo className="w-3.5 h-3.5 text-slate-400" /> Supporting Cluster Videos
              </span>
              <ul className="space-y-1.5 pl-2">
                {cluster.supporting_video_ideas.map((idea, idx) => (
                  <li key={idx} className="text-xs text-slate-300 flex items-start gap-2">
                    <span className="text-indigo-400 font-bold">•</span>
                    <span>{idea}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Playlist Suggestion */}
            <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span className="text-slate-400">Recommended Playlist:</span>
              <span className="font-semibold text-cyan-400">{cluster.playlist_suggestion}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
