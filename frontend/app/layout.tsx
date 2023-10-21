import "bootstrap/dist/css/bootstrap.min.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";

import { AuthProvider } from "./contexts/AuthContext";
import Header from "./components/Header";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "zoe-bot: the aspect of twighlight",
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
        <body className={inter.className}>
          <Header />
          {children}
        </body>
      </AuthProvider>
    </html>
  );
}
