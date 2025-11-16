import type { Metadata } from 'next'
import '../styles/globals.css'

export const metadata: Metadata = {
  title: 'Para Group Web UI',
  description: 'Analyze codebases with AI-powered insights',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body className="bg-dark-bg text-dark-text antialiased" suppressHydrationWarning>
        {children}
      </body>
    </html>
  )
}
