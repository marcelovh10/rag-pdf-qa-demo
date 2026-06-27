"use client";

import { useState } from "react";
import { Send, Loader2, ExternalLink } from "lucide-react";
import { query, Citation, QueryResponse } from "@/lib/api";

type Message = { role: "user" | "assistant"; content: string; data?: QueryResponse };

export function ChatWindow() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || loading) return;
    const question = input.trim();
    setInput("");
    setMessages((m) => [...m, { role: "user", content: question }]);
    setLoading(true);
    try {
      const result = await query(question);
      setMessages((m) => [...m, { role: "assistant", content: result.answer, data: result }]);
    } catch (e) {
      setMessages((m) => [
        ...m,
        { role: "assistant", content: `Error: ${e instanceof Error ? e.message : "Unknown"}` },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="rounded-xl border border-border bg-panel flex flex-col h-[600px]">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-zinc-500 text-sm py-12">
            Upload a PDF, then ask a question. Answers include citations.
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "flex justify-end" : "space-y-3"}>
            {m.role === "user" ? (
              <div className="bg-accent text-black rounded-lg px-3 py-2 max-w-[80%] text-sm">
                {m.content}
              </div>
            ) : (
              <div className="space-y-3">
                <div className="bg-zinc-900 rounded-lg px-3 py-2 text-sm whitespace-pre-wrap">
                  {m.content}
                </div>
                {m.data && m.data.citations.length > 0 && <CitationsPanel citations={m.data.citations} />}
                {m.data && (
                  <p className="text-xs text-zinc-500">
                    {m.data.usage.input_tokens + m.data.usage.output_tokens} tokens · ${m.data.estimated_cost_usd.toFixed(5)}
                  </p>
                )}
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex items-center gap-2 text-sm text-zinc-400">
            <Loader2 className="h-4 w-4 animate-spin" /> Thinking...
          </div>
        )}
      </div>

      <form onSubmit={onSubmit} className="border-t border-border p-3 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about the document..."
          className="flex-1 bg-zinc-900 border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="bg-accent text-black rounded-lg px-3 py-2 disabled:opacity-50 hover:bg-accent/90 transition"
        >
          <Send className="h-4 w-4" />
        </button>
      </form>
    </section>
  );
}

function CitationsPanel({ citations }: { citations: Citation[] }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border border-border rounded-lg overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full px-3 py-2 text-xs text-zinc-400 flex items-center justify-between hover:bg-zinc-900 transition"
      >
        <span>{citations.length} sources</span>
        <ExternalLink className="h-3 w-3" />
      </button>
      {open && (
        <div className="p-3 space-y-2 bg-zinc-950">
          {citations.map((c, i) => (
            <div key={c.chunk_id} className="text-xs text-zinc-400 border-l-2 border-accent pl-2">
              <div className="text-zinc-500">
                [{i + 1}] {c.source} · page {c.page ?? "?"} · score {c.score.toFixed(3)}
              </div>
              <div className="text-zinc-300 line-clamp-3 mt-1">{c.content}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
