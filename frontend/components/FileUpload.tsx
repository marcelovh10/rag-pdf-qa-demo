"use client";

import { useState } from "react";
import { Upload, CheckCircle2, Loader2 } from "lucide-react";
import { ingestPdf } from "@/lib/api";

type Status = "idle" | "uploading" | "done" | "error";

export function FileUpload() {
  const [status, setStatus] = useState<Status>("idle");
  const [filename, setFilename] = useState<string | null>(null);
  const [chunks, setChunks] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleFile(file: File) {
    setStatus("uploading");
    setError(null);
    setFilename(file.name);
    try {
      const result = await ingestPdf(file);
      setChunks(result.chunks_created);
      setStatus("done");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Upload failed");
      setStatus("error");
    }
  }

  return (
    <section className="rounded-xl border border-border bg-panel p-5 h-fit">
      <h2 className="font-medium mb-3">Upload PDF</h2>
      <label className="block">
        <input
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) handleFile(f);
          }}
        />
        <div className="border-2 border-dashed border-border rounded-lg p-6 text-center cursor-pointer hover:border-accent transition">
          {status === "uploading" ? (
            <Loader2 className="h-6 w-6 mx-auto animate-spin text-accent" />
          ) : (
            <Upload className="h-6 w-6 mx-auto text-zinc-500" />
          )}
          <p className="text-sm text-zinc-400 mt-2">
            {status === "uploading" ? "Processing..." : "Click to select a PDF"}
          </p>
        </div>
      </label>

      {status === "done" && filename && (
        <div className="mt-4 flex items-start gap-2 text-sm">
          <CheckCircle2 className="h-4 w-4 text-accent mt-0.5 shrink-0" />
          <div>
            <p className="text-zinc-200">{filename}</p>
            <p className="text-zinc-500 text-xs">{chunks} chunks indexed</p>
          </div>
        </div>
      )}

      {status === "error" && (
        <p className="mt-4 text-sm text-red-400">{error}</p>
      )}
    </section>
  );
}
