"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Sparkles, Building2, User, ArrowRight } from "lucide-react"

export default function HomePage() {
  const router = useRouter()
  const [userType, setUserType] = useState<"normal" | "business" | null>(null)

  const handleUserTypeSelect = (type: "normal" | "business") => {
    setUserType(type)

    if (type === "normal") {
      router.push("/image-generation")
    } else {
      router.push("/business-signup")
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gradient-to-b from-primary/10 to-background">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold tracking-tight mb-4 bg-gradient-to-r from-primary to-purple-400 bg-clip-text text-transparent">
          Content Creation Platform
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl">
          Generate stunning images, craft engaging descriptions, and manage your social media presence all in one place.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8 max-w-4xl w-full">
        <Card className="border-2 hover:border-primary/50 transition-all hover:shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5 text-primary" />
              Individual User
            </CardTitle>
            <CardDescription>Perfect for content creators, social media enthusiasts, and individuals</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="relative h-48 mb-4 rounded-lg overflow-hidden">
              <Image
                src="/placeholder.svg?height=400&width=600"
                alt="Individual features"
                fill
                className="object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end p-4">
                <p className="text-white text-sm">Generate images and descriptions for your personal content</p>
              </div>
            </div>
            <ul className="space-y-2 text-sm">
              <li className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-primary" />
                AI-powered image generation
              </li>
              <li className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-primary" />
                Engaging description creation
              </li>
              <li className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-primary" />
                Basic social media integration
              </li>
            </ul>
          </CardContent>
          <CardFooter>
            <Button className="w-full" onClick={() => handleUserTypeSelect("normal")}>
              Get Started
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </CardFooter>
        </Card>

        <Card className="border-2 hover:border-primary/50 transition-all hover:shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Building2 className="h-5 w-5 text-primary" />
              Business User
            </CardTitle>
            <CardDescription>Designed for businesses, agencies, and professional marketers</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="relative h-48 mb-4 rounded-lg overflow-hidden">
              <Image
                src="/placeholder.svg?height=400&width=600"
                alt="Business features"
                fill
                className="object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end p-4">
                <p className="text-white text-sm">Comprehensive tools for business content management</p>
              </div>
            </div>
            <ul className="space-y-2 text-sm">
              <li className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-primary" />
                Advanced analytics and trend prediction
              </li>
              <li className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-primary" />
                Sentiment analysis of comments
              </li>
              <li className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-primary" />
                Multi-platform social media management
              </li>
            </ul>
          </CardContent>
          <CardFooter>
            <Button className="w-full" onClick={() => handleUserTypeSelect("business")}>
              Business Sign Up
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </CardFooter>
        </Card>
      </div>

      <div className="mt-16 text-center text-sm text-muted-foreground">
        <p>
          Already have an account?{" "}
          <a href="/login" className="text-primary hover:underline">
            Log in
          </a>
        </p>
      </div>
    </div>
  )
}

