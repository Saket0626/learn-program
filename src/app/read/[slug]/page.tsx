import type { Metadata } from "next"
import Link from "next/link"
import { notFound } from "next/navigation"

import { MarkdownBody } from "@/components/markdown-body"
import { SiteShell } from "@/components/site-shell"
import { getPage, loadCourse } from "@/lib/manuscript"
import { prepareMarkdown } from "@/lib/prepare-markdown"

type Params = { slug: string }

export function generateStaticParams() {
  return loadCourse().pages.map((page) => ({ slug: page.slug }))
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>
}): Promise<Metadata> {
  const { slug } = await params
  const page = getPage(slug)
  return { title: page?.title ?? "Not found" }
}

export default async function ReadPage({ params }: { params: Promise<Params> }) {
  const { slug } = await params
  const course = loadCourse()
  const index = course.pages.findIndex((page) => page.slug === slug)
  const page = course.pages[index]
  if (!page) notFound()
  const previous = index > 0 ? course.pages[index - 1] : undefined
  const next = index < course.pages.length - 1 ? course.pages[index + 1] : undefined

  return (
    <SiteShell course={course}>
      <p className="font-sans text-xs tracking-wide text-muted-foreground uppercase">
        {page.partLabel ?? "Front matter"}
      </p>
      <article className="mt-3">
        <MarkdownBody markdown={prepareMarkdown(page.markdown)} />
      </article>
      <nav className="mt-12 grid gap-3 border-t border-border pt-6 sm:grid-cols-2">
        {previous ? (
          <Link
            href={`/read/${previous.slug}`}
            className="rounded-lg border border-border bg-card px-4 py-3 font-sans text-sm leading-snug hover:bg-accent"
          >
            <span className="text-xs tracking-wide text-muted-foreground uppercase">
              Previous
            </span>
            <span className="mt-1 block">{previous.title}</span>
          </Link>
        ) : (
          <span />
        )}
        {next ? (
          <Link
            href={`/read/${next.slug}`}
            className="rounded-lg border border-border bg-card px-4 py-3 font-sans text-sm leading-snug hover:bg-accent sm:text-right"
          >
            <span className="text-xs tracking-wide text-muted-foreground uppercase">
              Next
            </span>
            <span className="mt-1 block">{next.title}</span>
          </Link>
        ) : null}
      </nav>
    </SiteShell>
  )
}
