import fs from "fs"
import path from "path"

const STORE_DIR =
  "/cursor/stores/bc-2f3004f4-ad52-4cdc-a077-34046cf9404a/internal"

export type PageKind =
  | "front-matter"
  | "part-intro"
  | "section"
  | "chapter"
  | "glossary"
  | "readiness"

export type Page = {
  slug: string
  title: string
  kind: PageKind
  partNumber: number | null
  partLabel: string | null
  markdown: string
}

export type NavGroup = {
  label: string
  pages: Pick<Page, "slug" | "title" | "kind">[]
}

export type Course = {
  directory: string
  sourceFiles: string[]
  pages: Page[]
  groups: NavGroup[]
}

type SliceHint = "front" | "bridge" | "section"

function hasPartFiles(directory: string): boolean {
  try {
    return fs.readdirSync(directory).some((name) => /^part-.*\.md$/i.test(name))
  } catch {
    return false
  }
}

export function manuscriptDirectory(): string {
  const fromEnv = process.env.MANUSCRIPT_DIR
  if (fromEnv && hasPartFiles(fromEnv)) return fromEnv
  if (hasPartFiles(STORE_DIR)) return STORE_DIR
  return path.join(process.cwd(), "content", "manuscript")
}

function fileKey(name: string): { part: number; suffix: string } {
  const match = /^part-(\d+)([a-z]*)\.md$/i.exec(name)
  if (!match) return { part: 10000, suffix: name.toLowerCase() }
  return { part: Number(match[1]), suffix: match[2].toLowerCase() }
}

export function listPartFiles(directory: string): string[] {
  return fs
    .readdirSync(directory)
    .filter((name) => /^part-.*\.md$/i.test(name))
    .sort((a, b) => {
      const left = fileKey(a)
      const right = fileKey(b)
      if (left.part !== right.part) return left.part - right.part
      if (left.suffix !== right.suffix) return left.suffix < right.suffix ? -1 : 1
      return a < b ? -1 : a > b ? 1 : 0
    })
}

function headingLevel(text: string): number | null {
  const match = /^(#{1,6})\s+\S/.exec(text)
  return match ? match[1].length : null
}

type Line = { start: number; text: string }

function linesOf(corpus: string): Line[] {
  const lines: Line[] = []
  let start = 0
  while (start < corpus.length) {
    const nl = corpus.indexOf("\n", start)
    if (nl === -1) {
      lines.push({ start, text: corpus.slice(start) })
      break
    }
    lines.push({ start, text: corpus.slice(start, nl) })
    start = nl + 1
  }
  return lines
}

function hasProse(chunk: string): boolean {
  let inFence = false
  for (const line of chunk.split("\n")) {
    if (line.startsWith("```")) {
      inFence = !inFence
      continue
    }
    if (inFence || line.trim() === "") continue
    if (headingLevel(line) !== null) continue
    return true
  }
  return false
}

function firstHeadingText(markdown: string, level: number): string | null {
  let inFence = false
  for (const line of markdown.split("\n")) {
    if (line.startsWith("```")) {
      inFence = !inFence
      continue
    }
    if (inFence) continue
    const match = /^(#{1,6})\s+(.+?)\s*$/.exec(line)
    if (match && match[1].length === level) return match[2].trim()
  }
  return null
}

function bridgeTitle(markdown: string): string {
  let inFence = false
  let partTitle: string | null = null
  let firstH1: string | null = null
  for (const line of markdown.split("\n")) {
    if (line.startsWith("```")) {
      inFence = !inFence
      continue
    }
    if (inFence) continue
    if (/^# Part \d+:\s+\S/.test(line)) {
      partTitle = line.replace(/^#\s+/, "").trim()
    }
    const h1 = /^#\s+(.+?)\s*$/.exec(line)
    if (h1 && !line.startsWith("##") && !firstH1) firstH1 = h1[1].trim()
  }
  return partTitle ?? firstH1 ?? "Introduction"
}

function slugify(value: string): string {
  const slug = value
    .toLowerCase()
    .replace(/['’]/g, "")
    .replace(/&/g, " and ")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
  return slug || "section"
}

function classify(title: string, hint: SliceHint): PageKind {
  if (hint === "front") return "front-matter"
  if (/^Chapter\s+\d/.test(title)) return "chapter"
  if (/glossary/i.test(title)) return "glossary"
  if (/readiness/i.test(title)) return "readiness"
  if (hint === "bridge") return "part-intro"
  return "section"
}

function absorbPart(
  markdown: string,
  current: { number: number | null; label: string | null },
) {
  let inFence = false
  for (const line of markdown.split("\n")) {
    if (line.startsWith("```")) {
      inFence = !inFence
      continue
    }
    if (inFence) continue
    const match = /^# Part (\d+):\s+(.+)$/.exec(line)
    if (match) {
      current.number = Number(match[1])
      current.label = `Part ${match[1]}: ${match[2].trim()}`
    }
  }
}

function parseCorpus(corpus: string): { markdown: string; hint: SliceHint }[] {
  const lines = linesOf(corpus)
  let inFence = false
  let frontEnd = corpus.length
  const breaks: { at: number; level: 1 | 2 }[] = []

  for (const line of lines) {
    if (line.text.startsWith("```")) {
      inFence = !inFence
      continue
    }
    if (inFence) continue
    if (frontEnd === corpus.length && /^# Part \d+:\s+\S/.test(line.text)) {
      frontEnd = line.start
    }
    if (line.start < frontEnd) continue
    const level = headingLevel(line.text)
    if (level === 1 || level === 2) breaks.push({ at: line.start, level })
  }

  const slices: { markdown: string; hint: SliceHint }[] = [
    { markdown: corpus.slice(0, frontEnd), hint: "front" },
  ]

  let mode: "bridge" | "section" = "bridge"
  let bridgeStart = frontEnd
  let sectionStart = frontEnd

  const emit = (start: number, end: number, hint: SliceHint) => {
    if (end > start) slices.push({ markdown: corpus.slice(start, end), hint })
  }

  for (const item of breaks) {
    if (item.level === 1) {
      if (mode === "section") {
        emit(sectionStart, item.at, "section")
        mode = "bridge"
        bridgeStart = item.at
      }
      continue
    }

    if (mode === "bridge") {
      const bridge = corpus.slice(bridgeStart, item.at)
      if (hasProse(bridge)) {
        emit(bridgeStart, item.at, "bridge")
        sectionStart = item.at
      } else {
        sectionStart = bridgeStart
      }
      mode = "section"
      continue
    }

    emit(sectionStart, item.at, "section")
    sectionStart = item.at
  }

  if (mode === "section") emit(sectionStart, corpus.length, "section")
  else if (corpus.length > bridgeStart) emit(bridgeStart, corpus.length, "bridge")

  return slices.filter((slice) => slice.markdown.length > 0)
}

function titleFor(slice: { markdown: string; hint: SliceHint }): string {
  if (slice.hint === "front") return "Front matter"
  if (slice.hint === "bridge") return bridgeTitle(slice.markdown)
  return firstHeadingText(slice.markdown, 2) ?? bridgeTitle(slice.markdown)
}

export function parseCourse(directory: string, sourceFiles: string[]): Course {
  const corpus = sourceFiles
    .map((name) => fs.readFileSync(path.join(directory, name), "utf8"))
    .join("")
  const slices = parseCorpus(corpus)
  const used = new Set<string>()
  const part = { number: null as number | null, label: null as string | null }
  const pages: Page[] = []

  for (const slice of slices) {
    absorbPart(slice.markdown, part)
    const title = titleFor(slice)
    const kind = classify(title, slice.hint)
    let base = kind === "front-matter" ? "front-matter" : slugify(title)
    let slug = base
    let n = 2
    while (used.has(slug)) {
      slug = `${base}-${n}`
      n += 1
    }
    used.add(slug)
    pages.push({
      slug,
      title,
      kind,
      partNumber: kind === "front-matter" ? null : part.number,
      partLabel: kind === "front-matter" ? null : part.label,
      markdown: slice.markdown,
    })
  }

  const groups: NavGroup[] = []
  for (const page of pages) {
    const label = page.kind === "front-matter" ? "Front matter" : (page.partLabel ?? "Course")
    const last = groups[groups.length - 1]
    if (!last || last.label !== label) groups.push({ label, pages: [] })
    groups[groups.length - 1].pages.push({
      slug: page.slug,
      title: page.title,
      kind: page.kind,
    })
  }

  return { directory, sourceFiles, pages, groups }
}

let cached: { key: string; course: Course } | null = null

export function loadCourse(): Course {
  const directory = manuscriptDirectory()
  const sourceFiles = listPartFiles(directory)
  const key = sourceFiles
    .map((name) => {
      const stat = fs.statSync(path.join(directory, name))
      return `${name}:${stat.size}:${stat.mtimeMs}`
    })
    .join("|")
  if (cached && cached.key === key) return cached.course
  const course = parseCourse(directory, sourceFiles)
  cached = { key, course }
  return course
}

export function getPage(slug: string): Page | undefined {
  return loadCourse().pages.find((page) => page.slug === slug)
}
