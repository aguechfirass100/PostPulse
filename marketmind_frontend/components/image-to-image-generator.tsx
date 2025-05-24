/* components/image-to-image-generator.tsx */

"use client"

import { useState } from "react"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Input } from "@/components/ui/input"
import { Download, Share2, Sparkles } from "lucide-react"
import { API_ENDPOINTS } from '@/config/apiEndpoints'
import { toast } from "@/components/ui/use-toast"

// Token estimation constants
const FIXED_STYLE_TOKENS = 8
const SAFETY_MARGIN = 5
const MAX_USER_PROMPT_TOKENS = 77 - FIXED_STYLE_TOKENS - SAFETY_MARGIN
const estimateTokenCount = (text: string) => Math.ceil(text.length / 4)

// Option arrays
const toneOptions = [
  "Luxurious",
  "Playful",
  "Minimalist",
  "Bold & Colorful",
  "Elegant",
  "Futuristic",
]
const goalOptions = [
  "product promotion",
  "event announcement",
  "brand awareness",
  "limited time offer",
]
const callToActions = ["Shop Now", "Learn More", "Sign Up", "Get Started"]
const visualOptions = [
  "Product-centered",
  "Lifestyle background",
  "Urban environment",
  "Natural lighting",
  "Abstract graphics",
  "People using the product",
]

export function ImageToImageGenerator() {
  // Prompt-builder state
  const [brandName, setBrandName] = useState("")
  const [productName, setProductName] = useState("")
  const [includedDate, setIncludedDate] = useState("")
  const [selectedTone, setSelectedTone] = useState("")
  const [selectedGoal, setSelectedGoal] = useState("")
  const [selectedCTA, setSelectedCTA] = useState("")
  const [selectedVisuals, setSelectedVisuals] = useState<string[]>([])
  const [prompt, setPrompt] = useState("")

  // Image-to-image state
  const [inputImage, setInputImage] = useState<string | null>(null)
  const [style, setStyle] = useState("realistic")
  const [format, setFormat] = useState("square")
  const [creativity, setCreativity] = useState(50)
  const [generating, setGenerating] = useState(false)
  const [generatedImage, setGeneratedImage] = useState<string | null>(null)

  // Build prompt
  const generatePromptFromOptions = () => {
    const parts: string[] = []
    if (brandName) parts.push(`for the brand ${brandName}`)
    if (productName) parts.push(`highlighting the product ${productName}`)
    if (includedDate) parts.push(`with the date ${includedDate}`)
    if (selectedTone) parts.push(`in a ${selectedTone.toLowerCase()} tone`)
    if (selectedGoal) parts.push(`for ${selectedGoal}`)
    if (selectedCTA) parts.push(`featuring the call to action '${selectedCTA}'`)
    if (selectedVisuals.length) parts.push(`including visuals: ${selectedVisuals.join(", ")}`)
    setPrompt(`Transform this image ${parts.join(", ")}.`)
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) setInputImage(URL.createObjectURL(file))
  }

  const handleGenerate = async () => {
    if (!prompt || !inputImage) {
      toast({ title: "Error", description: "Provide both prompt & source image", variant: "destructive" })
      return
    }
    const tokenCount = estimateTokenCount(prompt)
    if (tokenCount > MAX_USER_PROMPT_TOKENS) {
      toast({ title: "Prompt Too Long", description: `~${tokenCount} tokens (max ${MAX_USER_PROMPT_TOKENS})`, variant: "destructive" })
      return
    }

    setGenerating(true)
    setGeneratedImage(null)
    try {
      const dims = {
        square: { width: 512, height: 512 }, portrait: { width: 512, height: 640 },
        landscape: { width: 1024, height: 576 }, story: { width: 576, height: 1024 },
      }[format] || { width: 512, height: 512 }

      const styledPrompt = `${prompt}, ${{
        realistic: "realistic photography, 8k, ultra detailed",
        cartoon: "cartoon style, vibrant colors",
        "3d": "3D render, blender, octane render",
        minimalist: "minimalist design, simple, clean lines",
        watercolor: "watercolor painting style",
      }[style]}`

      const form = new FormData()
      form.append('prompt', styledPrompt)
      form.append('image', inputImage)
      form.append('width', String(dims.width))
      form.append('height', String(dims.height))
      form.append('guidance_scale', String(3 + creativity / 50))

      const res = await fetch(`${API_ENDPOINTS.iMAGE_TO_IMAGE_GENERATOR}/transform`, { method: "POST", body: form })
      if (!res.ok) throw new Error()
      const blob = await res.blob()
      setGeneratedImage(URL.createObjectURL(blob))
      toast({ title: "Success", description: "Image transformed successfully" })
    } catch {
      toast({ title: "Error", description: "Generation failed. Try again.", variant: "destructive" })
    } finally { setGenerating(false) }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Card>
        <CardContent className="p-6 space-y-4">
          <h3 className="text-lg font-medium">Image-to-Image Transformation</h3>

          <div>
            <Label>Source Image</Label>
            {inputImage ? (
              <div className="relative w-full h-64 border rounded overflow-hidden">
                <Image src={inputImage} alt="Source" fill className="object-cover" />
                <button
                  onClick={() => setInputImage(null)}
                  className="absolute top-2 right-2 bg-white rounded-full p-1 shadow"
                >
                  ✕
                </button>
              </div>
            ) : (
              <label className="block w-full h-64 border-2 border-dashed border-muted-foreground rounded flex items-center justify-center cursor-pointer hover:border-primary">
                <input type="file" accept="image/*" className="hidden" onChange={handleFileChange} />
                <span className="text-muted-foreground">Click or drag to upload</span>
              </label>
            )}
          </div>

          {/* Prompt Builder */}
          <div className="grid grid-cols-2 gap-4">
            <Input placeholder="Brand name" value={brandName} onChange={e => setBrandName(e.target.value)} />
            <Input placeholder="Product name" value={productName} onChange={e => setProductName(e.target.value)} />
            <Input placeholder="Date (optional)" value={includedDate} onChange={e => setIncludedDate(e.target.value)} />
            <Select onValueChange={setSelectedTone}>
              <SelectTrigger><SelectValue placeholder="Brand Tone" /></SelectTrigger>
              <SelectContent>{toneOptions.map(t => <SelectItem key={t} value={t}>{t}</SelectItem>)}</SelectContent>
            </Select>
            <Select onValueChange={setSelectedGoal}>
              <SelectTrigger><SelectValue placeholder="Goal" /></SelectTrigger>
              <SelectContent>{goalOptions.map(g => <SelectItem key={g} value={g}>{g}</SelectItem>)}</SelectContent>
            </Select>
            <Select onValueChange={setSelectedCTA}>
              <SelectTrigger><SelectValue placeholder="Call to Action" /></SelectTrigger>
              <SelectContent>{callToActions.map(c => <SelectItem key={c} value={c}>{c}</SelectItem>)}</SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label>Visual Elements</Label>
            <div className="max-h-48 overflow-y-auto rounded-md border p-2 space-y-2">
              {visualOptions.map(option => (
                <label key={option} className="flex items-center space-x-2 p-2 hover:bg-accent rounded cursor-pointer">
                  <input type="checkbox" checked={selectedVisuals.includes(option)} onChange={e => {
                    const arr = selectedVisuals.includes(option)
                      ? selectedVisuals.filter(v => v !== option)
                      : [...selectedVisuals, option]
                    setSelectedVisuals(arr)
                  }} className="h-4 w-4 rounded border-primary text-primary focus:ring-primary" />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>
          <Button onClick={generatePromptFromOptions} className="w-full">Generate Prompt</Button>

          {/* Prompt Textarea */}
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <Label htmlFor="prompt">Prompt</Label>
              <span className="text-sm text-muted-foreground">{estimateTokenCount(prompt)}/{MAX_USER_PROMPT_TOKENS} tokens</span>
            </div>
            <Textarea id="prompt" value={prompt} onChange={e => setPrompt(e.target.value)} className="min-h-32" />
          </div>
          {/* Style & Format */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="style">Style</Label>
                <Select defaultValue="realistic" onValueChange={setStyle}>
                  <SelectTrigger id="style">
                    <SelectValue placeholder="Style" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="realistic">Realistic</SelectItem>
                    <SelectItem value="cartoon">Cartoon</SelectItem>
                    <SelectItem value="3d">3D Render</SelectItem>
                    <SelectItem value="minimalist">Minimalist</SelectItem>
                    <SelectItem value="watercolor">Watercolor</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="format">Format</Label>
                <Select defaultValue="square" onValueChange={setFormat}>
                  <SelectTrigger id="format">
                    <SelectValue placeholder="Format" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="square">Square (1:1)</SelectItem>
                    <SelectItem value="portrait">Portrait (4:5)</SelectItem>
                    <SelectItem value="landscape">Landscape (16:9)</SelectItem>
                    <SelectItem value="story">Story (9:16)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Creativity Slider & Generate Button */}
            <div className="space-y-2">
              <div className="flex justify-between">
                <Label htmlFor="creativity">Creativity Level</Label>
                <span className="text-sm text-muted-foreground">{creativity}%</span>
              </div>
              <Slider
                id="creativity"
                value={[creativity]}
                max={100}
                step={1}
                onValueChange={(val) => setCreativity(val[0])}
                className="py-4"
              />
            </div>
            <Button
              onClick={handleGenerate}
              disabled={!prompt || !inputImage || generating}
              className="w-full"
            >
              {generating ? (
                <>Processing...</>
              ) : (
                <>
                  <Sparkles className="mr-2 h-4 w-4" />
                  Transform Image
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Output Preview */}
      <Card>
        <CardContent className="p-6 flex items-center justify-center h-full">
          {generatedImage ? (
            <div className="w-full space-y-4">
              <div className="relative aspect-square w-full overflow-hidden rounded-lg border">
                <Image src={generatedImage} alt="Transformed" fill className="object-cover" />
              </div>
              <div className="flex justify-between">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    const link = document.createElement('a')
                    link.href = generatedImage!
                    link.download = `transformed-${Date.now()}.png`
                    document.body.appendChild(link)
                    link.click()
                    document.body.removeChild(link)
                  }}
                >
                  <Download className="mr-2 h-4 w-4" />
                  Download
                </Button>
                <Button variant="outline" size="sm">
                  <Share2 className="mr-2 h-4 w-4" />
                  Share
                </Button>
              </div>
            </div>
          ) : (
            <div className="text-center p-12 border-2 border-dashed rounded-lg border-muted-foreground/20 w-full h-full flex items-center justify-center">
              <Sparkles className="h-8 w-8 text-primary/40 mb-2" />
              <p className="text-muted-foreground">Your transformed image will appear here</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

