"use client"

import { Check, Copy } from "lucide-react"
import { useState } from "react"

export function CodeBlock({
  code,
  html,
  language,
}: {
  code: string
  html: string
  language?: string
}) {
  const [copied, setCopied] = useState(false)

  async function copy() {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      window.setTimeout(() => setCopied(false), 1500)
    } catch {
      setCopied(false)
    }
  }

  return (
    <div className="not-prose my-6 overflow-hidden rounded-lg border border-border bg-[#efe6d6]">
      <div className="flex items-center justify-between border-b border-border/70 px-3 py-1.5 font-sans text-xs text-muted-foreground">
        <span>{language || "code"}</span>
        <button
          type="button"
          onClick={copy}
          className="inline-flex items-center gap-1 rounded px-1.5 py-0.5 hover:bg-accent"
        >
          {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <pre className="overflow-x-auto px-4 py-3 text-[0.92rem] leading-6">
        <code dangerouslySetInnerHTML={{ __html: html }} />
      </pre>
    </div>
  )
}
