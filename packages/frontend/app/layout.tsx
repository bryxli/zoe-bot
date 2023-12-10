import "bootstrap/dist/css/bootstrap.min.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";

import { AuthProvider } from "./contexts/AuthContext";
import { GuildProvider } from "./contexts/GuildContext";

import "./app.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "zoe: the aspect of twighlight",
  description: "zoe bot web application",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <AuthProvider>
        <GuildProvider>
          <body className={inter.className}>{children}</body>
        </GuildProvider>
      </AuthProvider>
    </html>
  );
}
