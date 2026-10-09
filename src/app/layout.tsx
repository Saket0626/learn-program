import type { Metadata } from "next"
import { Source_Sans_3, Source_Serif_4 } from "next/font/google"
import "katex/dist/katex.min.css"

import "./globals.css"

const sans = Source_Sans_3({
  subsets: ["latin"],
  variable: "--font-sans",
})

const serif = Source_Serif_4({
  subsets: ["latin"],
  variable: "--font-serif",
})

export const metadata: Metadata = {
  title: {
    default: "From Zero to LeetCode Hard",
    template: "%s · From Zero to LeetCode Hard",
  },
  description:
    "A Python study paper that starts from no programming experience and builds through data structures, algorithms, worked LeetCode problems, and a training plan.",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${sans.variable} ${serif.variable}`}>
      <body className="font-sans antialiased">{children}</body>
    </html>
  )
}
