import type { Metadata } from "next";
import { Inter } from "next/font/google";

import "bootstrap/dist/css/bootstrap.min.css";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";

import "./app.css";

if (process.env.NODE_ENV === "development") {
  const config = require("@/../../configs/config.json");

  process.env["APPLICATION_ID"] = config.application_id;
  process.env["TOKEN"] = config.token;
  process.env["RIOT_API_KEY"] = config.riot_key;
}

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
