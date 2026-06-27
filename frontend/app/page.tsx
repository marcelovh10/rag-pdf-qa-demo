import { ChatWindow } from "@/components/ChatWindow";
import { FileUpload } from "@/components/FileUpload";
import { FileText } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen px-4 py-8 md:px-8 max-w-5xl mx-auto">
      <header className="mb-8 flex items-center gap-3">
        <div className="h-10 w-10 rounded-lg bg-accent flex items-center justify-center">
          <FileText className="h-5 w-5 text-black" />
        </div>
        <div>
          <h1 className="text-2xl font-semibold">RAG PDF QA</h1>
          <p className="text-sm text-zinc-400">Upload a PDF, ask a question, get cited answers.</p>
        </div>
      </header>

      <div className="grid gap-6 md:grid-cols-[1fr_2fr]">
        <FileUpload />
        <ChatWindow />
      </div>

      <footer className="mt-12 text-xs text-zinc-500 text-center">
        Built with Next.js · FastAPI · LangChain · pgvector · Groq · v2
      </footer>
    </main>
  );
}
