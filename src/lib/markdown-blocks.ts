export type MarkdownBlock =
  | { type: "md"; text: string }
  | { type: "answers"; headingRaw: string; text: string }

type LineInfo = { start: number; next: number; text: string }

function lineInfos(markdown: string): LineInfo[] {
  const lines: LineInfo[] = []
  let start = 0
  while (start < markdown.length) {
    const nl = markdown.indexOf("\n", start)
    if (nl === -1) {
      lines.push({ start, next: markdown.length, text: markdown.slice(start) })
      break
    }
    lines.push({ start, next: nl + 1, text: markdown.slice(start, nl) })
    start = nl + 1
  }
  return lines
}

export function splitBlocks(markdown: string): MarkdownBlock[] {
  const lines = lineInfos(markdown)
  const blocks: MarkdownBlock[] = []
  let mdStart = 0
  let inFence = false
  let index = 0

  while (index < lines.length) {
    const line = lines[index]
    if (line.text.startsWith("```")) {
      inFence = !inFence
      index += 1
      continue
    }

    const heading =
      !inFence && /^(#{2,6})\s+Answers and explanations\s*$/.exec(line.text)
    if (!heading) {
      index += 1
      continue
    }

    if (line.start > mdStart) {
      blocks.push({ type: "md", text: markdown.slice(mdStart, line.start) })
    }

    const level = heading[1].length
    let end = markdown.length
    let probe = index + 1
    let innerFence = false
    while (probe < lines.length) {
      const candidate = lines[probe]
      if (candidate.text.startsWith("```")) {
        innerFence = !innerFence
        probe += 1
        continue
      }
      if (!innerFence) {
        const nextHeading = /^(#{1,6})\s+\S/.exec(candidate.text)
        if (nextHeading && nextHeading[1].length <= level) {
          end = candidate.start
          break
        }
      }
      probe += 1
    }

    blocks.push({
      type: "answers",
      headingRaw: markdown.slice(line.start, line.next),
      text: markdown.slice(line.next, end),
    })
    mdStart = end
    if (end >= markdown.length) break
    const nextIndex = lines.findIndex((item) => item.start === end)
    index = nextIndex === -1 ? lines.length : nextIndex
    inFence = false
  }

  if (mdStart < markdown.length) {
    blocks.push({ type: "md", text: markdown.slice(mdStart) })
  }
  return blocks
}

export function reconstructBlocks(markdown: string): string {
  return splitBlocks(markdown)
    .map((block) =>
      block.type === "md" ? block.text : block.headingRaw + block.text,
    )
    .join("")
}
