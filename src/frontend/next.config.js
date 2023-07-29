const path = require("path");

/** @type {import('next').NextConfig} */
const nextConfig = {
  // NOTE: This was annoying, so turned off.
  reactStrictMode: false,
  output: "standalone",
  experimental: {
    outputFileTracingRoot: path.join(__dirname, "../../"),
  },
  images: {
    domains: ["storage.googleapis.com"],
  },
};

module.exports = nextConfig;
