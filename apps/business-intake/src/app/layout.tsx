import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Business Automation Intake | Fraser Tech',
  description: 'Tell us about your business. We\'ll figure out how to simplify it.',
  openGraph: {
    title: 'Business Automation Intake',
    description: 'Streamline your local business with custom automation',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
