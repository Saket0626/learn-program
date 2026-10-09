const ANSWER_HEADING = "\n### Answers and explanations\n\n"

export function prepareMarkdown(source: string): string {
  const withAnswers = source
    .replace(
      /<details>\s*<summary>\s*(?:Answers and explanations|Example answers and evaluation criteria)\s*<\/summary>/gi,
      ANSWER_HEADING,
    )
    .replace(/<\/details>/gi, "\n")

  return withAnswers
    .split(/(```[\s\S]*?```)/g)
    .map((chunk) => {
      if (chunk.startsWith("```")) return chunk
      return chunk
        .replace(/\\\[([\s\S]+?)\\\]/g, (_, expression: string) => {
          return `\n$$\n${expression.trim()}\n$$\n`
        })
        .replace(/\\\(([\s\S]+?)\\\)/g, (_, expression: string) => {
          return `$${expression}$`
        })
    })
    .join("")
}
