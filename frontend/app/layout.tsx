import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RAG PDF QA — Ask Your Documents",
  description: "Production RAG system with citation-aware answers.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-bg text-zinc-100 antialiased">{children}</body>
    </html>
  );
}
