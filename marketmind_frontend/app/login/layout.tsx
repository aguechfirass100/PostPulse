// app/signup/layout.tsx
import { Inter } from "next/font/google";
const inter = Inter({ subsets: ["latin"] });

export default function LoginLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <main>
          {children}
        </main>
      </body>
    </html>
  );
}
