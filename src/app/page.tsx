import Link from "next/link"

import { SiteShell } from "@/components/site-shell"
import { loadCourse } from "@/lib/manuscript"

export default function HomePage() {
  const course = loadCourse()
  const front = course.pages.find((page) => page.kind === "front-matter")
  const firstChapter =
    course.pages.find((page) => page.kind === "chapter") ?? course.pages[1]

  return (
    <SiteShell course={course}>
      <p className="font-sans text-xs tracking-wide text-muted-foreground uppercase">
        Course reader
      </p>
      <h1 className="mt-2 font-serif text-4xl font-medium tracking-tight">
        From Zero to LeetCode Hard
      </h1>
      <p className="mt-4 leading-8">
        Eight parts, from a first Python program through fully worked LeetCode
        problems and a 40-week training plan. Parts 1–6 are the original
        manuscript. Parts 7 and 8 continue it.
      </p>
      <div className="mt-8 flex flex-wrap gap-3">
        {front ? (
          <Link
            href={`/read/${front.slug}`}
            className="rounded-lg border border-border bg-card px-4 py-3 font-sans text-sm hover:bg-accent"
          >
            Read the front matter
          </Link>
        ) : null}
        {firstChapter ? (
          <Link
            href={`/read/${firstChapter.slug}`}
            className="rounded-lg border border-border bg-primary px-4 py-3 font-sans text-sm text-white hover:opacity-90"
          >
            Start at {firstChapter.title}
          </Link>
        ) : null}
      </div>
      <h2 className="mt-12 font-serif text-2xl font-medium">Code companions</h2>
      <ul className="mt-3 list-disc space-y-2 pl-5">
        <li>
          <a className="text-primary underline underline-offset-2" href="/code/part5_algorithms.py">
            part5_algorithms.py
          </a>
        </li>
        <li>
          <a className="text-primary underline underline-offset-2" href="/code/part7_solutions.py">
            part7_solutions.py
          </a>
        </li>
      </ul>
    </SiteShell>
  )
}
