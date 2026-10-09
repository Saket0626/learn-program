import Link from "next/link"

export default function NotFound() {
  return (
    <main className="mx-auto max-w-xl px-6 py-24">
      <h1 className="font-serif text-3xl">Page not found</h1>
      <Link href="/" className="mt-6 inline-block text-sm text-primary underline">
        Back to the contents
      </Link>
    </main>
  )
}
