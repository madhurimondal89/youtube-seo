"use client";

import React, { useState } from "react";
import { FileText, Download, FileSpreadsheet, FileCode, CheckCircle2 } from "lucide-react";
import { researchKeyword } from "@/lib/api";
import { exportKeywordsToCSV, exportToJSON, exportToMarkdown } from "@/lib/export";

export default function ReportsPage() {
  const [seed, setSeed] = useState("youtube automation");
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleExport = async (format: "csv" | "json" | "md") => {
    if (!seed.trim()) return;
    setLoading(true);
    setStatus(`Generating ${format.toUpperCase()} export...`);
    try {
      const res = await researchKeyword(seed, true, true, 30);
      if (format === "csv") exportKeywordsToCSV(res, `report_${seed}`);
      else if (format === "json") exportToJSON(res, `report_${seed}`);
      else if (format === "md") exportToMarkdown(res, `report_${seed}`);
      setStatus(`Export downloaded successfully!`);
      setTimeout(() => setStatus(null), 3000);
    } catch {
      setStatus("Export failed. Please check network or seed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Exportable Research Reports</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Download self-contained CSV, JSON, and Markdown reports with full algorithmic transparency and data provenance.
        </p>
      </div>

      <div className="glass-panel p-6 space-y-4 max-w-xl">
        <div>
          <label className="block text-xs font-semibold text-slate-300 mb-1.5">Target Research Seed</label>
          <input
            type="text"
            value={seed}
            onChange={(e) => setSeed(e.target.value)}
            className="w-full bg-slate-900/90 border border-slate-700/80 rounded-lg px-3.5 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div className="flex flex-col sm:flex-row gap-3 pt-2">
          <button
            onClick={() => handleExport("csv")}
            disabled={loading}
            className="flex-1 px-4 py-2.5 rounded-lg bg-slate-900 hover:bg-slate-800 disabled:opacity-50 border border-slate-700 text-xs font-semibold text-slate-200 flex items-center justify-center gap-2"
          >
            <FileSpreadsheet className="w-4 h-4 text-emerald-400" />
            <span>Export CSV</span>
          </button>
          <button
            onClick={() => handleExport("json")}
            disabled={loading}
            className="flex-1 px-4 py-2.5 rounded-lg bg-slate-900 hover:bg-slate-800 disabled:opacity-50 border border-slate-700 text-xs font-semibold text-slate-200 flex items-center justify-center gap-2"
          >
            <FileCode className="w-4 h-4 text-indigo-400" />
            <span>Export JSON</span>
          </button>
          <button
            onClick={() => handleExport("md")}
            disabled={loading}
            className="flex-1 px-4 py-2.5 rounded-lg bg-slate-900 hover:bg-slate-800 disabled:opacity-50 border border-slate-700 text-xs font-semibold text-slate-200 flex items-center justify-center gap-2"
          >
            <FileText className="w-4 h-4 text-cyan-400" />
            <span>Export Markdown</span>
          </button>
        </div>

        {status && <p className="text-xs text-emerald-400 font-medium pt-1">{status}</p>}
      </div>
    </div>
  );
}
