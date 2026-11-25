import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  async rewrites() {
    // In Coolify/Docker internal network, INTERNAL_BACKEND_URL is http://backend:8000
    // In local development, fallback to http://127.0.0.1:8000
    const backendUrl = process.env.INTERNAL_BACKEND_URL || "http://127.0.0.1:8000";
    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
