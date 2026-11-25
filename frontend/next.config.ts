import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  async rewrites() {
    // In Coolify/Docker internal network, INTERNAL_BACKEND_URL is http://backend:8000 or http://127.0.0.1:8001
    // In local development or unified container, fallback to http://127.0.0.1:8001
    const backendUrl = process.env.INTERNAL_BACKEND_URL || "http://127.0.0.1:8001";
    return [
      {
        source: "/health",
        destination: `${backendUrl}/health`,
      },
      {
        source: "/api/:path*",
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
