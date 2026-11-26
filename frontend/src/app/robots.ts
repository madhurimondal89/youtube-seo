import { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://tubepilot.ai";

  return {
    rules: [
      // General search engine crawlers
      {
        userAgent: "*",
        allow: [
          "/",
          "/keywords",
          "/video-audit",
          "/outliers",
          "/competitors",
          "/content-gaps",
          "/thumbnail-analyzer",
          "/growth-coach",
          "/ai-studio",
          "/calendar",
          "/reports",
          "/topics",
          "/channel-audit",
          "/llms.txt",
          "/llms-full.txt",
        ],
        disallow: [
          "/api/",
          "/settings",
          "/api-setup",
          "/_next/",
        ],
      },
      // AI & LLM Search Crawlers (Explicitly Allowed for GEO)
      {
        userAgent: [
          "GPTBot",
          "ChatGPT-User",
          "ClaudeBot",
          "PerplexityBot",
          "Google-Extended",
          "Applebot-Extended",
          "cohere-ai",
          "Bytespider",
          "CCBot",
        ],
        allow: [
          "/",
          "/keywords",
          "/video-audit",
          "/outliers",
          "/competitors",
          "/content-gaps",
          "/thumbnail-analyzer",
          "/growth-coach",
          "/ai-studio",
          "/calendar",
          "/reports",
          "/topics",
          "/channel-audit",
          "/llms.txt",
          "/llms-full.txt",
        ],
        disallow: ["/api/", "/settings", "/api-setup"],
      },
    ],
    sitemap: `${siteUrl}/sitemap.xml`,
  };
}
