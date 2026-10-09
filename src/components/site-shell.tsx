import Link from "next/link"

import { CourseNav } from "@/components/course-nav"
import { MobileBar } from "@/components/mobile-bar"
import type { Course } from "@/lib/manuscript"

export function SiteShell({
  course,
  children,
}: {
  course: Course
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen">
      <div className="mx-auto grid max-w-7xl lg:grid-cols-[18rem_minmax(0,1fr)]">
        <aside className="sticky top-0 hidden h-screen overflow-y-auto border-r border-border bg-card lg:block">
          <div className="border-b border-border px-5 py-5">
            <Link href="/" className="font-serif text-lg leading-tight">
              From Zero to LeetCode Hard
            </Link>
            <p className="mt-1 font-sans text-xs text-muted-foreground">Course reader</p>
          </div>
          <CourseNav groups={course.groups} />
        </aside>
        <div className="min-w-0">
          <MobileBar groups={course.groups} />
          <div className="mx-auto max-w-3xl px-5 py-8 sm:px-8 sm:py-12">{children}</div>
        </div>
      </div>
    </div>
  )
}
