import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/layout/Sidebar";
import TopBar from "@/components/layout/TopBar";

export const metadata: Metadata = {
  title: "TubePilot AI — Self-Hosted Creator Intelligence Platform",
  description:
    "Production-grade, transparent YouTube keyword research, competition analysis, opportunity scoring, outlier detection, and video audit platform.",
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
