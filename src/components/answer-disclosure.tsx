"use client"

import { ChevronDown } from "lucide-react"
import type { ReactNode } from "react"

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"

export function AnswerDisclosure({ children }: { children: ReactNode }) {
  return (
    <Collapsible className="my-6 overflow-hidden rounded-lg border border-border bg-card">
      <CollapsibleTrigger className="group flex w-full items-center justify-between gap-3 px-4 py-3 text-left font-sans text-sm font-medium">
        <span>Answers and explanations</span>
        <ChevronDown className="h-4 w-4 shrink-0 transition-transform group-data-[state=open]:rotate-180" />
      </CollapsibleTrigger>
      <CollapsibleContent
        forceMount
        className="border-t border-border data-[state=closed]:hidden"
      >
        <div className="px-4 py-4 sm:px-5">{children}</div>
      </CollapsibleContent>
    </Collapsible>
  )
}
