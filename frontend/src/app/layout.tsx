import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { SidebarLayout } from "@/components/Layout";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AcquireIQ - Deal Sourcing",
  description: "AI-powered M&A Deal Sourcing Pipeline",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="min-h-screen bg-slate-50 antialiased">
      <body className={`${inter.className} min-h-screen`}>
        <SidebarLayout>{children}</SidebarLayout>
      </body>
    </html>
  );
}
