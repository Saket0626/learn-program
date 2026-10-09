import ReactMarkdown from "react-markdown"
import rehypeKatex from "rehype-katex"
import remarkGfm from "remark-gfm"
import remarkMath from "remark-math"
import type { ReactNode } from "react"

import { AnswerDisclosure } from "@/components/answer-disclosure"
import { CodeBlock } from "@/components/code-block"
import { highlightCode } from "@/lib/highlight"
import { splitBlocks } from "@/lib/markdown-blocks"

const proseClass =
  "prose prose-stone max-w-none prose-headings:font-serif prose-headings:font-medium prose-headings:tracking-tight prose-p:leading-8 prose-li:leading-7 prose-a:text-primary prose-code:rounded prose-code:bg-[#efe6d6] prose-code:px-1.5 prose-code:py-0.5 prose-code:font-mono prose-code:text-[0.9em] prose-code:font-normal prose-code:text-foreground prose-code:before:content-none prose-code:after:content-none"

function textContent(node: ReactNode): string {
  if (node == null || typeof node === "boolean") return ""
  if (typeof node === "string" || typeof node === "number") return String(node)
  if (Array.isArray(node)) return node.map(textContent).join("")
  if (typeof node === "object" && "props" in node) {
    const element = node as { props?: { children?: ReactNode } }
    return textContent(element.props?.children)
  }
  return ""
}

function languageOf(node: ReactNode): string | undefined {
  if (node == null || typeof node === "boolean") return undefined
  if (typeof node === "string" || typeof node === "number") return undefined
  if (Array.isArray(node)) {
    for (const child of node) {
      const found = languageOf(child)
      if (found) return found
    }
    return undefined
  }
  if (typeof node === "object" && "props" in node) {
    const element = node as {
      props?: { className?: string; children?: ReactNode }
    }
    const className = element.props?.className
    const match = className && /language-([\w+-]+)/.exec(className)
    if (match) return match[1]
    return languageOf(element.props?.children)
  }
  return undefined
}

function FencedPre({ children }: { children?: ReactNode }) {
  const code = textContent(children).replace(/\n$/, "")
  const language = languageOf(children)
  return (
    <CodeBlock
      code={code}
      html={highlightCode(code, language)}
      language={language}
    />
  )
}

function MarkdownChunk({ markdown }: { markdown: string }) {
  if (markdown.trim() === "") return null
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm, remarkMath]}
      rehypePlugins={[rehypeKatex]}
      components={{
        pre: ({ children }) => <FencedPre>{children}</FencedPre>,
        table: ({ children }) => (
          <div className="not-prose my-6 overflow-x-auto rounded-lg border border-border">
            <table className="w-full min-w-[36rem] border-collapse font-sans text-sm">
              {children}
            </table>
          </div>
        ),
        th: ({ children }) => (
          <th className="border-b border-border bg-secondary px-3 py-2 text-left align-bottom font-semibold">
            {children}
          </th>
        ),
        td: ({ children }) => (
          <td className="border-b border-border px-3 py-2 align-top">{children}</td>
        ),
        a: ({ href, children }) => (
          <a
            href={href}
            className="text-primary underline decoration-primary/30 underline-offset-2"
          >
            {children}
          </a>
        ),
      }}
    >
      {markdown}
    </ReactMarkdown>
  )
}

export function MarkdownBody({ markdown }: { markdown: string }) {
  const blocks = splitBlocks(markdown)
  return (
    <div>
      {blocks.map((block, index) =>
        block.type === "answers" ? (
          <AnswerDisclosure key={index}>
            <div className={proseClass}>
              <MarkdownChunk markdown={block.text} />
            </div>
          </AnswerDisclosure>
        ) : (
          <div key={index} className={proseClass}>
            <MarkdownChunk markdown={block.text} />
          </div>
        ),
      )}
    </div>
  )
}
