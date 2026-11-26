import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "18-Point YouTube Video SEO Audit & Optimization Checker",
  description:
    "Comprehensive 18-point video SEO checker. Audit title length, keyword placement, description structure, chapter timestamps, and tags to maximize YouTube rankings.",
  alternates: {
    canonical: "/video-audit",
  },
  openGraph: {
    title: "18-Point Video SEO Audit — TubePilot AI",
    description:
      "Audit live YouTube videos or drafts across 18 ranking factors with actionable category scores and recommendations.",
    url: "/video-audit",
  },
};

export default function VideoAuditLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
