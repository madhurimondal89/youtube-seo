"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { fetchSystemStatus } from "@/lib/api";
import { SystemStatus } from "@/lib/types";
import {
  LayoutDashboard,
  Search,
  Compass,
  Users,
  TrendingUp,
  Layers,
  Video,
  UserCheck,
  Sparkles,
  Calendar,
  FileText,
  Settings,
  Image as ImageIcon,
  GraduationCap,
} from "lucide-react";

const NAV_ITEMS = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Keyword Research", href: "/keywords", icon: Search },
  { name: "Topic Explorer", href: "/topics", icon: Compass },
  { name: "Competitors", href: "/competitors", icon: Users },
  { name: "Outliers", href: "/outliers", icon: TrendingUp },
  { name: "Content Gaps", href: "/content-gaps", icon: Layers },
  { name: "Thumbnail Vision", href: "/thumbnail-analyzer", icon: ImageIcon },
  { name: "Video Audit", href: "/video-audit", icon: Video },
  { name: "Channel Audit", href: "/channel-audit", icon: UserCheck },
  { name: "AI Studio", href: "/ai-studio", icon: Sparkles },
  { name: "Growth Coach", href: "/growth-coach", icon: GraduationCap },
  { name: "Content Calendar", href: "/calendar", icon: Calendar },
  { name: "Reports", href: "/reports", icon: FileText },
  { name: "Settings", href: "/settings", icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [status, setStatus] = useState<SystemStatus | null>(null);

  useEffect(() => {
    fetchSystemStatus().then((s) => {
      if (s) setStatus(s);
    });
  }, []);

  return (
    <aside className="w-64 h-screen fixed left-0 top-0 border-r border-[var(--color-rule)] bg-[var(--color-paper-3)] flex flex-col z-30">
      {/* Brand Header */}
      <div className="h-16 px-6 flex items-center gap-3 border-b border-[var(--color-rule)]">
        <div className="w-9 h-9 rounded-md bg-[var(--color-paper-2)] border border-[var(--color-rule-2)] flex items-center justify-center">
          <svg className="w-5 h-5 text-red-500 fill-current" viewBox="0 0 24 24">
            <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
          </svg>
        </div>
        <div className="flex flex-col">
          <span className="font-semibold text-base text-[var(--color-ink)] leading-snug">
            YouTube SEO
          </span>
          <span className="text-xs text-[var(--color-muted)] font-normal">
            Creator intelligence
          </span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3.5 py-2.5 rounded-md text-sm font-medium transition-colors duration-150 ${
                isActive
                  ? "bg-[var(--color-paper-2)] text-[var(--color-ink)] border border-[var(--color-rule-2)]"
                  : "text-[var(--color-muted)] hover:text-[var(--color-ink)] hover:bg-[var(--color-paper-2)]/60"
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? "text-[var(--color-accent)]" : "text-[var(--color-muted)]"}`} />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer / System Status */}
      <div className="p-4 border-t border-[var(--color-rule)]">
        <div className="p-3 rounded-md bg-[var(--color-paper-2)] border border-[var(--color-rule)] flex flex-col gap-1.5">
          <div className="flex items-center justify-between text-xs">
            <span className="text-[var(--color-muted)]">Engine Mode</span>
            <span className="text-[var(--color-ok)] font-medium">Stateless Core</span>
          </div>
          <div className="text-[11px] text-[var(--color-muted)] flex items-center justify-between">
            <span>AI Status</span>
            <span className={`font-medium ${
              status?.ai_mode === "AI Connected"
                ? "text-emerald-400"
                : status?.ai_mode === "Hybrid Mode"
                ? "text-amber-400"
                : "text-cyan-400"
            }`}>
              {status?.ai_mode === "AI Connected"
                ? "AI Connected"
                : status?.ai_mode === "Hybrid Mode"
                ? "Hybrid Fallback"
                : "Deterministic"}
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}
