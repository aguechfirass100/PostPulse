"use client"

import type React from "react"

import { useState, useRef } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { ArrowLeft, Building2, CheckCircle2, Upload} from "lucide-react"
import { API_ENDPOINTS } from '@/config/apiEndpoints'

export default function BusinessSignupPage() {
  const router = useRouter()
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [currentStep, setCurrentStep] = useState(1)
  const [formData, setFormData] = useState({
    businessName: "",
    industry: "",
    size: "",
    website: "",
    description: "",
    goals: "",
    platforms: "",
    email: "",
    password: "",
    confirmPassword: "",
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSelectChange = (name: string, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }))
  }
  // Upload PDF and extract only step-1 fields
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    const data = new FormData()
    data.append('file', file)

    const res = await fetch(`${API_ENDPOINTS.PDF_PARSER}/extract`, {
      method: 'POST',
      body: data,
    })
    const json = await res.json()

    // Only map step 1 fields
    const { businessName, industry, size, website, description } = json
    setFormData(prev => ({
      ...prev,
      businessName: businessName || prev.businessName,
      industry: industry || prev.industry,
      size: size || prev.size,
      website: website || prev.website,
      description: description || prev.description,
    }))

    // Download JSON of extracted step1 data
    const step1Data = { businessName, industry, size, website, description }
    const blob = new Blob([JSON.stringify(step1Data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'business_info_step1.json'
    a.click()
    URL.revokeObjectURL(url)
  }

  const handleNextStep = () => {
    setCurrentStep((prev) => prev + 1)
  }

  const handlePrevStep = () => {
    setCurrentStep((prev) => prev - 1)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // In a real app, you would submit the form data to your backend
    router.push("/")
  }

  return (
  <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gradient-to-b from-primary/10 to-background">
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Building2 className="h-5 w-5 text-primary" />
          Business Account Setup
        </CardTitle>
        <CardDescription>Tell us about your business to get started with our platform</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex justify-between mb-8">
          {[1, 2, 3].map((step) => (
            <div
              key={step}
              className={`flex flex-col items-center ${currentStep >= step ? "text-primary" : "text-muted-foreground"}`}
            >
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center border-2 ${
                  currentStep > step
                    ? "bg-primary border-primary text-primary-foreground"
                    : currentStep === step
                      ? "border-primary text-primary"
                      : "border-muted-foreground text-muted-foreground"
                }`}
              >
                {currentStep > step ? <CheckCircle2 className="h-5 w-5" /> : step}
              </div>
              <span className="text-xs mt-1">
                {step === 1 ? "Business Info" : step === 2 ? "Social Media" : "Account"}
              </span>
            </div>
          ))}
        </div>

        <form onSubmit={e => e.preventDefault()}>
          {currentStep === 1 && (
            <div className="space-y-4">
              {/* PDF Upload Section */}
              <div className="flex items-center space-x-4">
                <Button variant="outline" onClick={() => fileInputRef.current?.click()}>
                  <Upload className="mr-2 h-4 w-4" />
                  Upload PDF
                </Button>
                <input
                  type="file"
                  accept="application/pdf"
                  hidden
                  ref={fileInputRef}
                  onChange={handleFileUpload}
                />
              </div>
              
              {/* Form Fields Section */}
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="businessName">Business Name</Label>
                    <Input
                      id="businessName"
                      name="businessName"
                      value={formData.businessName}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="industry">Industry</Label>
                    <Select value={formData.industry} onValueChange={(value) => handleSelectChange("industry", value)}>
                      <SelectTrigger id="industry">
                        <SelectValue placeholder="Select industry" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="technology">Technology</SelectItem>
                        <SelectItem value="retail">Retail</SelectItem>
                        <SelectItem value="healthcare">Healthcare</SelectItem>
                        <SelectItem value="finance">Finance</SelectItem>
                        <SelectItem value="education">Education</SelectItem>
                        <SelectItem value="other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="size">Company Size</Label>
                    <Select value={formData.size} onValueChange={(value) => handleSelectChange("size", value)}>
                      <SelectTrigger id="size">
                        <SelectValue placeholder="Select size" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1-10">1-10 employees</SelectItem>
                        <SelectItem value="11-50">11-50 employees</SelectItem>
                        <SelectItem value="51-200">51-200 employees</SelectItem>
                        <SelectItem value="201-500">201-500 employees</SelectItem>
                        <SelectItem value="501+">501+ employees</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="website">Website</Label>
                    <Input
                      id="website"
                      name="website"
                      value={formData.website}
                      onChange={handleInputChange}
                      placeholder="https://"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">Business Description</Label>
                  <Textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    placeholder="Tell us about your business..."
                    className="min-h-[100px]"
                  />
                </div>
              </div>
            </div>
          )}

            {currentStep === 2 && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="goals">Social Media Goals</Label>
                  <Textarea
                    id="goals"
                    name="goals"
                    value={formData.goals}
                    onChange={handleInputChange}
                    placeholder="What are your main goals for social media marketing?"
                    className="min-h-[100px]"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="platforms">Current Social Media Platforms</Label>
                  <Select value={formData.platforms} onValueChange={(value) => handleSelectChange("platforms", value)}>
                    <SelectTrigger id="platforms">
                      <SelectValue placeholder="Select primary platform" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="instagram">Instagram</SelectItem>
                      <SelectItem value="facebook">Facebook</SelectItem>
                      <SelectItem value="twitter">Twitter</SelectItem>
                      <SelectItem value="linkedin">LinkedIn</SelectItem>
                      <SelectItem value="tiktok">TikTok</SelectItem>
                      <SelectItem value="youtube">YouTube</SelectItem>
                      <SelectItem value="none">None yet</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            )}

            {currentStep === 3 && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email Address</Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <Input
                    id="password"
                    name="password"
                    type="password"
                    value={formData.password}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">Confirm Password</Label>
                  <Input
                    id="confirmPassword"
                    name="confirmPassword"
                    type="password"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>
            )}
          </form>
        </CardContent>
        <CardFooter className="flex justify-between">
          {currentStep > 1 ? (
            <Button variant="outline" onClick={handlePrevStep}>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
          ) : (
            <Button variant="outline" onClick={() => router.push("/")}>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Cancel
            </Button>
          )}

          {currentStep < 3 ? (
            <Button onClick={handleNextStep}>Continue</Button>
          ) : (
            <Button onClick={() => router.push("/")}>Complete Setup</Button>
          )}
        </CardFooter>
      </Card>
    </div>
  )
}

