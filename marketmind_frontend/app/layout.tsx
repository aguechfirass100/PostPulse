import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import AuthWrapper from "./AuthWrapper";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Content Creation Platform",
  description: "A modern platform for content creation and social media management",
  generator: "v0.dev",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthWrapper>{children}</AuthWrapper>
      </body>
    </html>
  );
}




// import type React from "react"
// import type { Metadata } from "next"
// import { Inter } from "next/font/google"
// import "./globals.css"
// import { Sidebar } from "@/components/sidebar"
// import { AuthProvider } from './contexts/AuthContext';


// const inter = Inter({ subsets: ["latin"] })

// export const metadata: Metadata = {
//   title: "Content Creation Platform",
//   description: "A modern platform for content creation and social media management",
//     generator: 'v0.dev'
// }

// export default function RootLayout({
//   children,
// }: Readonly<{
//   children: React.ReactNode
// }>) {
//   return (
//     <html lang="en">
//       <body className={inter.className}>
//         <AuthProvider>
//           <div className="flex min-h-screen">
//             <Sidebar />
//             <main className="flex-1 overflow-auto">{children}</main>
//           </div>
//         </AuthProvider>
//       </body>
//     </html>
//   )
// }

