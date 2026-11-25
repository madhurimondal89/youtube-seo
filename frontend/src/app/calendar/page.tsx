"use client";

import React, { useState, useEffect } from "react";
import { Calendar as CalendarIcon, Clock, Sparkles, Download } from "lucide-react";
import { generateCalendar } from "@/lib/api";

export default function CalendarPage() {
  const [topic, setTopic] = useState("YouTube Growth Strategy");
  const [duration, setDuration] = useState(30);
  const [schedule, setSchedule] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchCalendar = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await generateCalendar(topic, duration);
      setSchedule(res?.schedule || []);
    } catch (err: any) {
      setError(err.message || "Failed to generate content calendar.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCalendar();
  }, [duration]);

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Content Calendar</h1>
          <p className="text-xs sm:text-sm text-slate-400">
            Publishing schedules balancing hero pillars, high-intent evergreen guides, and trend captures.
          </p>
        </div>

        <div className="flex gap-2">
          {[7, 30, 60, 90].map((days) => (
            <button
              key={days}
              onClick={() => setDuration(days)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                duration === days ? "bg-indigo-600 text-white" : "bg-slate-900 text-slate-400 hover:text-slate-200"
              }`}
            >
              {days} Days
            </button>
          ))}
        </div>
      </div>

      {/* Input */}
      <div className="glass-panel p-5">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            fetchCalendar();
          }}
          className="flex flex-col sm:flex-row gap-3"
        >
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Niche or content pillar..."
            className="flex-1 bg-slate-900/90 border border-slate-700/80 rounded-lg px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm flex items-center gap-2"
          >
            <CalendarIcon className="w-4 h-4" />
            <span>{loading ? "Planning..." : "Generate Calendar"}</span>
          </button>
        </form>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm">
          {error}
        </div>
      )}

      {loading && (
        <div className="p-8 text-center glass-card rounded-xl border border-slate-800 space-y-2">
          <div className="inline-block w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-xs text-slate-400">Balancing pillars, evergreen topics, and publishing roadmap...</p>
        </div>
      )}

      {!loading && schedule.length === 0 && !error && (
        <div className="p-8 text-center glass-panel rounded-xl text-slate-400 text-sm">
          No calendar generated yet. Enter a niche or content pillar above and click Generate Calendar.
        </div>
      )}

      {/* Calendar Roadmap Timeline */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {schedule.map((item, i) => (
          <div key={i} className="glass-card p-5 rounded-xl border border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-indigo-400 bg-indigo-950/50 px-2.5 py-0.5 rounded border border-indigo-800/40">
                Day {item.day}
              </span>
              <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-semibold">
                {item.content_type}
              </span>
            </div>

            <h3 className="text-sm font-bold text-white leading-snug">{item.title}</h3>

            <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
              <span>Keyword: <strong className="text-slate-200">{item.target_keyword}</strong></span>
              <span>Intent: <strong className="text-cyan-400">{item.intent}</strong></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
