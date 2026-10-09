function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
}

export function highlightCode(code: string, language?: string): string {
  const escaped = escapeHtml(code)
  if (language === "text" || !language) return escaped
  return escaped
    .replace(
      /(^|\n)(\s*#(?!\[)[^\n]*)/g,
      '$1<span class="tok-comment">$2</span>',
    )
    .replace(
      /(&quot;(?:\\.|[^&])*?&quot;|&#39;(?:\\.|[^&])*?&#39;)/g,
      '<span class="tok-string">$1</span>',
    )
}
