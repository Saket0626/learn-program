"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"

import type { NavGroup } from "@/lib/manuscript"
import { cn } from "@/lib/utils"

export function CourseNav({ groups }: { groups: NavGroup[] }) {
  const pathname = usePathname()

  return (
    <nav className="space-y-6 px-3 py-4">
      {groups.map((group) => (
        <div key={group.label}>
          <p className="px-2 text-xs tracking-wide text-muted-foreground uppercase">
            {group.label}
          </p>
          <ul className="mt-1 space-y-0.5">
            {group.pages.map((page) => {
              const href = `/read/${page.slug}`
              const active = pathname === href
              return (
                <li key={page.slug}>
                  <Link
                    href={href}
                    data-active={active ? "true" : "false"}
                    className={cn(
                      "block rounded-md px-2 py-1.5 font-sans text-sm leading-snug hover:bg-accent",
                      active && "bg-accent font-medium text-foreground",
                    )}
                  >
                    {page.title}
                  </Link>
                </li>
              )
            })}
          </ul>
        </div>
      ))}
    </nav>
  )
}
