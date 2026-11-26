import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "YouTube Keyword Research & Multi-Vector Autocomplete Tool",
  description:
    "Free YouTube keyword expansion tool. Discover long-tail search queries with A-Z alphabet expansion, 9-category search intent, relative demand, and estimated competition scores.",
  alternates: {
    canonical: "/keywords",
  },
  openGraph: {
    title: "YouTube Keyword Research Tool — TubePilot AI",
    description:
      "Find high-opportunity YouTube keywords with live public autocomplete expansion, demand scores, and competition analysis.",
    url: "/keywords",
  },
};

export default function KeywordsLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
