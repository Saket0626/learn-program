"use client"

import { Menu, X } from "lucide-react"
import { useState } from "react"

import { CourseNav } from "@/components/course-nav"
import type { NavGroup } from "@/lib/manuscript"

export function MobileBar({ groups }: { groups: NavGroup[] }) {
  const [open, setOpen] = useState(false)

  return (
    <div className="border-b border-border bg-card lg:hidden">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="flex w-full items-center gap-2 px-4 py-3 font-sans text-sm"
      >
        {open ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
        Contents
      </button>
      {open ? (
        <div className="max-h-[70vh] overflow-y-auto border-t border-border" onClick={() => setOpen(false)}>
          <CourseNav groups={groups} />
        </div>
      ) : null}
    </div>
  )
}
