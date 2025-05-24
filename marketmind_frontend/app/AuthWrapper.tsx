"use client";

import { usePathname } from "next/navigation";
import { Sidebar } from "@/components/sidebar";
import { AuthProvider } from "./contexts/AuthContext";

export default function AuthWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  // No sidebar on /login and /signup
  const noSidebarRoutes = ["/login", "/signup"];
  const hideSidebar = noSidebarRoutes.includes(pathname);

  return (
    <AuthProvider>
      {hideSidebar ? (
        <main className="min-h-screen">{children}</main>
      ) : (
        <div className="flex min-h-screen">
          <Sidebar />
          <main className="flex-1 overflow-auto">{children}</main>
        </div>
      )}
    </AuthProvider>
  );
}
