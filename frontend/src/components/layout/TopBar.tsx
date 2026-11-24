"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Search, Cpu, Database, Check } from "lucide-react";
import { fetchSystemStatus } from "@/lib/api";
import { SystemStatus } from "@/lib/types";

export default function TopBar() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState<SystemStatus | null>(null);

  useEffect(() => {
    fetchSystemStatus().then((s) => {
      if (s) setStatus(s);
    });
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/keywords?seed=${encodeURIComponent(query.trim())}`);
    }
  };

  return (
    <header className="h-16 border-b border-[var(--color-rule)] bg-[var(--color-paper)] fixed top-0 right-0 left-64 z-20 px-6 flex items-center justify-between gap-4">
      {/* Global Quick Search Bar */}
      <form onSubmit={handleSearch} className="flex-1 max-w-lg relative">
        <Search className="w-4 h-4 text-[var(--color-muted)] absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Research keyword or video URL (e.g. 'youtube automation')..."
          className="w-full bg-[var(--color-paper-2)] border border-[var(--color-rule)] rounded-md pl-9 pr-4 py-2 text-sm text-[var(--color-ink)] placeholder-[var(--color-muted)] focus:outline-none focus:border-[var(--color-rule-2)] focus:ring-1 focus:ring-[var(--color-focus)] transition-colors duration-150"
        />
      </form>

      {/* Telemetry & System Status Badges */}
      <div className="flex items-center gap-3">
        {/* Data Provider Mode */}
        <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-[var(--color-paper-2)] border border-[var(--color-rule)] text-xs">
          <Database className="w-3.5 h-3.5 text-[var(--color-cool)]" />
          <span className="text-[var(--color-muted)]">Data:</span>
          <span className="font-medium text-[var(--color-ink)] capitalize">
            {status?.youtube_provider || "Public Web"}
          </span>
        </div>

        {/* AI Layer Mode */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-[var(--color-paper-2)] border border-[var(--color-rule)] text-xs">
          <Cpu className="w-3.5 h-3.5 text-[var(--color-accent)]" />
          <span className="text-[var(--color-muted)]">AI:</span>
          <span className={`font-medium ${status?.ai_enabled ? "text-[var(--color-ok)]" : "text-[var(--color-muted)]"}`}>
            {status?.ai_enabled ? status.ai_status : "Deterministic"}
          </span>
        </div>

        {/* Backend Heartbeat */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-[var(--color-ok-soft)] border border-[var(--color-rule)] text-xs text-[var(--color-ok)]">
          <Check className="w-3.5 h-3.5" />
          <span className="font-medium">Active</span>
        </div>
      </div>
    </header>
  );
}
