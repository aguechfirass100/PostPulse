"use client"

import { useState } from "react"
import Link from "next/link"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { 
  ArrowRight, 
  CheckCircle2, 
  Sparkles, 
  Zap, 
  MessagesSquare, 
  TrendingUp, 
  PieChart, 
  MonitorSmartphone, 
  Video, 
  Image as ImageIcon,
  CircleUser,
  Building,
  Building2
} from "lucide-react"
import PricingSection from "@/components/PricingSection"

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Navigation */}
      <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 z-10">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link href="/" className="flex items-center space-x-2">
              <Sparkles className="h-6 w-6 text-primary" />
              <span className="font-bold text-xl">PostPulse</span>
            </Link>
          </div>
          <div className="hidden md:flex items-center space-x-4">
            <Link href="#features" className="text-sm font-medium hover:text-primary transition-colors">
              Features
            </Link>
            <Link href="#pricing" className="text-sm font-medium hover:text-primary transition-colors">
              Pricing
            </Link>
            <Link href="#testimonials" className="text-sm font-medium hover:text-primary transition-colors">
              Testimonials
            </Link>
            <Link href="/login" className="text-sm font-medium hover:text-primary transition-colors">
              Login
            </Link>
            <Button asChild>
              <Link href="/signup">Sign Up</Link>
            </Button>
          </div>
          <div className="flex md:hidden">
            <Button variant="ghost" className="px-2">
              <span className="sr-only">Open menu</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-6 w-6">
                <line x1="4" x2="20" y1="12" y2="12"></line>
                <line x1="4" x2="20" y1="6" y2="6"></line>
                <line x1="4" x2="20" y1="18" y2="18"></line>
              </svg>
            </Button>
          </div>
        </div>
      </nav>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="px-4 py-20 md:py-32 bg-gradient-to-b from-primary/10 to-background">
          <div className="container grid md:grid-cols-2 gap-8 items-center">
            <div className="flex flex-col space-y-6">
              <div>
                <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-4 bg-gradient-to-r from-primary to-purple-400 bg-clip-text text-transparent">
                  Elevate Your Social Media Presence
                </h1>
                <p className="text-xl text-muted-foreground max-w-md">
                  PostPulse helps you create engaging content, analyze performance, and stay ahead of social media trends.
                </p>
              </div>
              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <Button size="lg" asChild>
                  <Link href="/signup">Get Started for Free</Link>
                </Button>
                <Button size="lg" variant="outline" asChild>
                  <Link href="#features">Explore Features</Link>
                </Button>
              </div>
              <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                <div className="flex items-center">
                  <CheckCircle2 className="h-4 w-4 mr-1 text-primary" />
                  <span>No credit card required</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle2 className="h-4 w-4 mr-1 text-primary" />
                  <span>Free 14-day trial</span>
                </div>
              </div>
            </div>
            <div className="relative h-[400px] rounded-lg overflow-hidden shadow-xl border">
              <Image 
                src="/placeholder.svg?height=800&width=1200" 
                alt="PostPulse Dashboard" 
                fill 
                className="object-cover" 
              />
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-20 px-4">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold mb-4">Everything You Need for Social Media Success</h2>
              <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                PostPulse combines AI-powered content creation with advanced analytics to optimize your social media strategy.
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {/* Feature 1 */}
              <Card className="border shadow-sm hover:shadow-md transition-all">
                <CardHeader>
                  <Zap className="h-10 w-10 text-primary mb-2" />
                  <CardTitle>AI Content Generation</CardTitle>
                  <CardDescription>
                    Create engaging text for your social media posts in seconds.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Our advanced AI algorithms analyze top-performing content and craft personalized posts optimized for engagement.
                  </p>
                </CardContent>
              </Card>

              {/* Feature 2 */}
              <Card className="border shadow-sm hover:shadow-md transition-all">
                <CardHeader>
                  <ImageIcon className="h-10 w-10 text-primary mb-2" />
                  <CardTitle>Visual Content Creation</CardTitle>
                  <CardDescription>
                    Generate eye-catching images and transform product photos.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Create professional visual content with our easy-to-use image generation and editing tools.
                  </p>
                </CardContent>
              </Card>

              {/* Feature 3 */}
              <Card className="border shadow-sm hover:shadow-md transition-all">
                <CardHeader>
                  <Video className="h-10 w-10 text-primary mb-2" />
                  <CardTitle>Video Generation</CardTitle>
                  <CardDescription>
                    Turn images and prompts into engaging video content.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Create short-form videos for TikTok, Instagram Reels, and YouTube Shorts with just a few clicks.
                  </p>
                </CardContent>
              </Card>

              {/* Feature 4 */}
              <Card className="border shadow-sm hover:shadow-md transition-all">
                <CardHeader>
                  <MessagesSquare className="h-10 w-10 text-primary mb-2" />
                  <CardTitle>Sentiment Analysis</CardTitle>
                  <CardDescription>
                    Understand how your audience responds to your content.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Analyze comments and mentions to gauge audience sentiment and improve your content strategy.
                  </p>
                </CardContent>
              </Card>

              {/* Feature 5 */}
              <Card className="border shadow-sm hover:shadow-md transition-all">
                <CardHeader>
                  <TrendingUp className="h-10 w-10 text-primary mb-2" />
                  <CardTitle>Trend Prediction</CardTitle>
                  <CardDescription>
                    Stay ahead of social media trends before they go viral.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Our AI analyzes millions of posts to predict upcoming trends, helping you create timely content.
                  </p>
                </CardContent>
              </Card>

              {/* Feature 6 */}
              <Card className="border shadow-sm hover:shadow-md transition-all">
                <CardHeader>
                  <MonitorSmartphone className="h-10 w-10 text-primary mb-2" />
                  <CardTitle>Multi-Platform Integration</CardTitle>
                  <CardDescription>
                    Manage all your social accounts in one place.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Connect Instagram, TikTok, YouTube, Twitter, LinkedIn, and Facebook for seamless content management.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        {/* Who is it for Section */}
        <section className="py-20 px-4 bg-secondary">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold mb-4">Who is PostPulse For?</h2>
              <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                Our platform is designed to help anyone looking to improve their social media presence.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {/* User Type 1 */}
              <Card className="border shadow-sm hover:shadow-md transition-all">
                <CardHeader className="pb-4">
                  <CircleUser className="h-10 w-10 text-primary mb-2" />
                  <CardTitle>Content Creators & Influencers</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Save time creating engaging content while maintaining your authentic voice. Analyze what resonates with your audience to grow your following.
                  </p>
                </CardContent>
              </Card>

              {/* User Type 2 */}
              <Card className="border shadow-sm hover:shadow-md transition-all">
                <CardHeader className="pb-4">
                  <Building className="h-10 w-10 text-primary mb-2" />
                  <CardTitle>Small Businesses & Startups</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Compete with larger brands by creating professional social media content without the need for a dedicated marketing team.
                  </p>
                </CardContent>
              </Card>

              {/* User Type 3 */}
              <Card className="border shadow-sm hover:shadow-md transition-all">
                <CardHeader className="pb-4">
                  <Building2 className="h-10 w-10 text-primary mb-2" />
                  <CardTitle>Marketing Agencies</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Scale your client operations efficiently with our comprehensive toolkit and advanced analytics for multiple accounts.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        <PricingSection />

        {/* Testimonials */}
        <section id="testimonials" className="py-20 px-4 bg-secondary">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold mb-4">Loved by Creators and Businesses</h2>
              <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                See what our customers have to say about PostPulse.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {/* Testimonial 1 */}
              <Card className="border shadow-sm">
                <CardHeader>
                  <div className="flex items-center gap-4">
                    <div className="relative h-12 w-12 rounded-full overflow-hidden">
                      <Image 
                        src="/placeholder.svg?height=100&width=100" 
                        alt="Sarah Johnson" 
                        fill 
                        className="object-cover" 
                      />
                    </div>
                    <div>
                      <CardTitle className="text-lg">Sarah Johnson</CardTitle>
                      <CardDescription>Fitness Influencer</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    "PostPulse has transformed how I manage my social media. I save hours each week on content creation, and my engagement has increased by 45% since I started using it."
                  </p>
                </CardContent>
              </Card>

              {/* Testimonial 2 */}
              <Card className="border shadow-sm">
                <CardHeader>
                  <div className="flex items-center gap-4">
                    <div className="relative h-12 w-12 rounded-full overflow-hidden">
                      <Image 
                        src="/placeholder.svg?height=100&width=100" 
                        alt="Mark Thompson" 
                        fill 
                        className="object-cover" 
                      />
                    </div>
                    <div>
                      <CardTitle className="text-lg">Mark Thompson</CardTitle>
                      <CardDescription>CEO, Bright Startups</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    "As a small business owner, I couldn't afford a marketing team. PostPulse gave us the tools to compete with larger brands at a fraction of the cost. The ROI has been incredible."
                  </p>
                </CardContent>
              </Card>

              {/* Testimonial 3 */}
              <Card className="border shadow-sm">
                <CardHeader>
                  <div className="flex items-center gap-4">
                    <div className="relative h-12 w-12 rounded-full overflow-hidden">
                      <Image 
                        src="/placeholder.svg?height=100&width=100" 
                        alt="Anna Martinez" 
                        fill 
                        className="object-cover" 
                      />
                    </div>
                    <div>
                      <CardTitle className="text-lg">Anna Martinez</CardTitle>
                      <CardDescription>Marketing Director, SocialBoost Agency</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    "Managing multiple client accounts was overwhelming until we found PostPulse. Now we can scale our agency operations while delivering better results for our clients."
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-4 bg-gradient-to-r from-primary/20 to-purple-400/20">
          <div className="container text-center">
            <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Social Media Presence?</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
              Join thousands of creators and businesses who are already saving time and growing their audience with PostPulse.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Button size="lg" asChild>
                <Link href="/signup">Get Started for Free</Link>
              </Button>
              <Button size="lg" variant="outline" asChild>
                <Link href="/demo">Request a Demo</Link>
              </Button>
            </div>
            <p className="mt-4 text-sm text-muted-foreground">
              No credit card required. Free 14-day trial on all plans.
            </p>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t py-12 px-4">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-semibold mb-4">PostPulse</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link href="/about" className="text-muted-foreground hover:text-foreground transition-colors">
                    About Us
                  </Link>
                </li>
                <li>
                  <Link href="/careers" className="text-muted-foreground hover:text-foreground transition-colors">
                    Careers
                  </Link>
                </li>
                <li>
                  <Link href="/blog" className="text-muted-foreground hover:text-foreground transition-colors">
                    Blog
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link href="/features" className="text-muted-foreground hover:text-foreground transition-colors">
                    Features
                  </Link>
                </li>
                <li>
                  <Link href="/pricing" className="text-muted-foreground hover:text-foreground transition-colors">
                    Pricing
                  </Link>
                </li>
                <li>
                  <Link href="/roadmap" className="text-muted-foreground hover:text-foreground transition-colors">
                    Roadmap
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Resources</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link href="/help" className="text-muted-foreground hover:text-foreground transition-colors">
                    Help Center
                  </Link>
                </li>
                <li>
                  <Link href="/guides" className="text-muted-foreground hover:text-foreground transition-colors">
                    Guides & Tutorials
                  </Link>
                </li>
                <li>
                  <Link href="/api" className="text-muted-foreground hover:text-foreground transition-colors">
                    API Documentation
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Legal</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link href="/terms" className="text-muted-foreground hover:text-foreground transition-colors">
                    Terms of Service
                  </Link>
                </li>
                <li>
                  <Link href="/privacy" className="text-muted-foreground hover:text-foreground transition-colors">
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link href="/cookies" className="text-muted-foreground hover:text-foreground transition-colors">
                    Cookie Policy
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          
          <div className="mt-12 pt-8 border-t flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Sparkles className="h-5 w-5 text-primary" />
              <span className="font-bold">PostPulse</span>
            </div>
            <div className="flex space-x-6">
              <Link href="https://twitter.com" className="text-muted-foreground hover:text-foreground">
                <span className="sr-only">Twitter</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"></path>
                </svg>
              </Link>
              <Link href="https://instagram.com" className="text-muted-foreground hover:text-foreground">
                <span className="sr-only">Instagram</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                  <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                  <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                </svg>
              </Link>
              <Link href="https://linkedin.com" className="text-muted-foreground hover:text-foreground">
                <span className="sr-only">LinkedIn</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                  <rect x="2" y="9" width="4" height="12"></rect>
                  <circle cx="4" cy="4" r="2"></circle>
                </svg>
              </Link>
            </div>
          </div>
          
          <div className="mt-8 text-center text-sm text-muted-foreground">
            <p>© {new Date().getFullYear()} PostPulse. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
