import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Recruitment Copilot",
  description: "Premium AI Career Assistant & Upwork Proposal Generator",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-gray-950 text-white min-h-screen selection:bg-blue-600 selection:text-white`}>
        {children}
      </body>
    </html>
  );
}
