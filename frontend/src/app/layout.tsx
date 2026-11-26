import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/layout/Sidebar";
import TopBar from "@/components/layout/TopBar";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://seo.freeyoutubetools.com";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "TubePilot AI — Free YouTube SEO, Keyword Research & Creator Intelligence",
    template: "%s | TubePilot AI",
  },
  description:
    "Production-grade, transparent YouTube keyword research, competition analysis, opportunity scoring, outlier detection, and 18-point video SEO audit platform.",
  keywords: [
    "YouTube SEO",
    "YouTube Keyword Tool",
    "Free vidIQ Alternative",
    "Free TubeBuddy Alternative",
    "YouTube Video SEO Checker",
    "Viral Video Outlier Detection",
    "YouTube Tag Generator",
    "YouTube Competitor Analysis",
    "Creator Intelligence Platform",
    "YouTube Content Strategy AI",
  ],
  authors: [{ name: "TubePilot Team", url: siteUrl }],
  creator: "TubePilot AI",
  publisher: "TubePilot AI",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "TubePilot AI — Self-Hosted YouTube SEO & Creator Intelligence",
    description:
      "Independent creator intelligence platform. Transparent mathematical formulas for keyword opportunity scoring, 18-point video SEO audit, and viral outlier detection.",
    url: siteUrl,
    siteName: "TubePilot AI",
    locale: "en_US",
    type: "website",
    images: [
      {
        url: "/icon.png",
        width: 512,
        height: 512,
        alt: "TubePilot AI — Creator Intelligence Logo",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "TubePilot AI — YouTube SEO & Keyword Intelligence",
    description:
      "Deterministic YouTube keyword research, 18-point video SEO audit, and viral outlier detection without mandatory paid APIs.",
    images: ["/icon.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  icons: {
    icon: [
      { url: "/icon.png", type: "image/png" },
      { url: "/favicon.ico", sizes: "any" },
    ],
    apple: "/apple-icon.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // Global Schema.org Structured Data
  const globalSchema = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebApplication",
        "@id": `${siteUrl}/#software`,
        name: "TubePilot AI",
        url: siteUrl,
        applicationCategory: "BusinessApplication",
        operatingSystem: "All (Web-based)",
        description:
          "Self-hosted YouTube SEO, creator research, keyword opportunity scoring, and viral outlier detection platform.",
        offers: {
          "@type": "Offer",
          price: "0",
          priceCurrency: "USD",
          description: "Free and Open Creator Intelligence Software",
        },
        featureList: [
          "YouTube Autocomplete Multi-Vector Keyword Expansion",
          "10-Signal Keyword Opportunity Scoring",
          "18-Point Deterministic Video SEO Audit",
          "Median Absolute Deviation (MAD) Outlier Detection",
          "Competitor Channel Comparison and Content Gap Detection",
          "AI Studio Title, Description, and Retention Hook Ideation",
        ],
      },
      {
        "@type": "Organization",
        "@id": `${siteUrl}/#organization`,
        name: "TubePilot AI",
        url: siteUrl,
        logo: `${siteUrl}/icon.png`,
      },
      {
        "@type": "WebSite",
        "@id": `${siteUrl}/#website`,
        url: siteUrl,
        name: "TubePilot AI",
        potentialAction: {
          "@type": "SearchAction",
          target: {
            "@type": "EntryPoint",
            urlTemplate: `${siteUrl}/keywords?seed={search_term_string}`,
          },
          "query-input": "required name=search_term_string",
        },
      },
    ],
  };

  return (
    <html lang="en" className="dark h-full antialiased" suppressHydrationWarning>
      <head>
        <link rel="icon" href="/icon.png" type="image/png" />
        <link rel="apple-touch-icon" href="/apple-icon.png" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Mono:wght@400;500;700&family=Host+Grotesk:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
        {/* Global Structured Data JSON-LD */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(globalSchema) }}
        />
      </head>
      <body className="min-h-full bg-[var(--color-paper)] text-[var(--color-ink)] flex flex-col font-sans">
        <Sidebar />
        <TopBar />
        <main className="ml-64 pt-20 px-6 pb-12 md:px-8 md:pt-24 min-h-screen bg-[var(--color-paper)] flex-1">
          {children}
        </main>
      </body>
    </html>
  );
}
