import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Viral Video Outlier Finder — Median Absolute Deviation (MAD)",
  description:
    "Identify breakout YouTube videos that outperformed channel averages by 3x to 30x using statistical Median Absolute Deviation (MAD) outlier analysis.",
  alternates: {
    canonical: "/outliers",
  },
  openGraph: {
    title: "Viral Video Outlier Finder — TubePilot AI",
    description:
      "Discover proven breakout topics and viral video ideas with statistical outlier detection.",
    url: "/outliers",
  },
};

export default function OutliersLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
