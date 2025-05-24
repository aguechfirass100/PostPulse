"use client"

import type React from "react"

import { useState, useEffect } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Home, Image, FileText, Share2, BarChart2, MessageSquare, Settings, Menu, X ,Video } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

export function Sidebar() {
  const [isOpen, setIsOpen] = useState(false)
  const pathname = usePathname()

  // Close sidebar when path changes (mobile navigation)
  useEffect(() => {
    setIsOpen(false)
  }, [])

  const toggleSidebar = () => {
    setIsOpen(!isOpen)
  }

  // Don't show sidebar on home and business-signup pages
  if (pathname === "/" || pathname === "/business-signup") {
    return null
  }

  return (
    <>
      <Button variant="ghost" size="icon" className="fixed top-4 left-4 z-40 md:hidden" onClick={toggleSidebar}>
        {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
      </Button>

      <div
        className={cn(
          "fixed inset-y-0 left-0 z-30 w-64 bg-primary text-primary-foreground transform transition-transform duration-200 ease-in-out md:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="flex flex-col h-full">
          <div className="p-4 border-b border-primary-foreground/10">
            <h1 className="text-xl font-bold">Content Platform</h1>
          </div>

          <nav className="flex-1 p-4 space-y-1">
            <NavItem href="/" icon={<Home className="mr-2 h-5 w-5" />} label="Dashboard" />
            <NavItem href="/image-generation" icon={<Image className="mr-2 h-5 w-5" />} label="Image Generation" />
            <NavItem
              href="/video-generation"
              icon={<Video className="mr-2 h-5 w-5" />}
              label="Video Generation"
            />
            <NavItem
              href="/image-to-image-generation"
              icon={<Image className="mr-2 h-5 w-5" />}
              label="Image To Image Generation"
            />
            <NavItem
              href="/description-generation"
              icon={<FileText className="mr-2 h-5 w-5" />}
              label="Description Generation"
            />
            <NavItem href="/social-media" icon={<Share2 className="mr-2 h-5 w-5" />} label="Social Media" />
            <NavItem href="/trends" icon={<BarChart2 className="mr-2 h-5 w-5" />} label="Trend Analysis" />
            <NavItem href="/sentiment" icon={<MessageSquare className="mr-2 h-5 w-5" />} label="Sentiment Analysis" />
          </nav>

          <div className="p-4 border-t border-primary-foreground/10">
            <NavItem href="/settings" icon={<Settings className="mr-2 h-5 w-5" />} label="Settings" />
          </div>
        </div>
      </div>

      {/* Add padding to main content when sidebar is visible */}
      <div className="md:w-64 shrink-0"></div>
    </>
  )
}

function NavItem({ href, icon, label }: { href: string; icon: React.ReactNode; label: string }) {
  const pathname = usePathname()
  const isActive = pathname === href

  return (
    <Link
      href={href}
      className={cn(
        "flex items-center px-3 py-2 rounded-md transition-colors",
        isActive ? "bg-primary-foreground/20 text-primary-foreground font-medium" : "hover:bg-primary-foreground/10",
      )}
    >
      {icon}
      <span>{label}</span>
    </Link>
  )
}

