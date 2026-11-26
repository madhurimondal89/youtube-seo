import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Studio — YouTube Title, Description & Retention Hook Generator",
  description:
    "Generate high-CTR YouTube video titles, structured descriptions with chapter timestamps, and retention hook formulas powered by AI and proven creator templates.",
  alternates: {
    canonical: "/ai-studio",
  },
  openGraph: {
    title: "YouTube AI Creator Studio — TubePilot AI",
    description:
      "High-performing YouTube title ideation, hooks, tags, and chapter generators.",
    url: "/ai-studio",
  },
};

export default function AiStudioLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
