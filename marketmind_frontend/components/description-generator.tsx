"use client"

import React, { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { toast } from "@/components/ui/use-toast"
import { API_ENDPOINTS } from '@/config/apiEndpoints'
import { FileText } from "lucide-react"

export function DescriptionGenerator() {
  // Prompt builder state
  const [brand, setBrand] = useState<string>("")
  const [date, setDate] = useState<string>("")
  const [audience, setAudience] = useState<string[]>([])
  const [category, setCategory] = useState<string>("")
  const [includeCTA, setIncludeCTA] = useState<boolean>(false)
  const [ctaText, setCtaText] = useState<string>("")
  const [includeEmojis, setIncludeEmojis] = useState<boolean>(false)
  const [language, setLanguage] = useState<string>("English")
  const [tone, setTone] = useState<string>("Professional")
  const [hashtagInput, setHashtagInput] = useState<string>("")
  const [generatedPrompt, setGeneratedPrompt] = useState<string>("")

  // Description generator state
  const [length, setLength] = useState<string>("medium")
  const [includeHashtags, setIncludeHashtags] = useState<boolean>(true)
  const [generatedDescription, setGeneratedDescription] = useState<string | null>(null)
  const [generating, setGenerating] = useState<boolean>(false)

  const audienceOptions = [
    'Students', 'Professionals', 'Tech Enthusiasts', 'Parents', 'Fitness Fans'
  ]
  const toneOptions = ['Professional', 'Casual', 'Enthusiastic', 'Humorous', 'Inspirational']

  const handleAudienceChange = (opt: string) => {
    setAudience(prev =>
      prev.includes(opt) ? prev.filter(a => a !== opt) : [...prev, opt]
    )
  }

  const buildPrompt = () => {
    let prompt = `Generate a post description`;
    if (brand) prompt += ` for **${brand}**`;
    if (date) prompt += ` on **${date}**`;
    if (category) prompt += ` in the **${category}** category`;
    if (audience.length) prompt += ` targeted at ${audience.join(', ')}`;
    prompt += ` using a ${tone} tone in ${language}`;
    if (includeEmojis) prompt += ` with emojis`;
    if (includeCTA && ctaText) prompt += `, ending with "${ctaText}"`;
    if (hashtagInput) prompt += ` and include hashtags: ${hashtagInput}`;
    prompt += '.';
    return prompt;
  }

  const handleGeneratePrompt = () => {
    const prompt = buildPrompt()
    if (!prompt) {
      toast({ title: "Error", description: "Please fill in at least one field", variant: "destructive" })
      return
    }
    setGeneratedPrompt(prompt)
  }

  const handleGenerateDescription = async () => {
    if (!generatedPrompt) {
      toast({ title: "Error", description: "Generate a prompt first", variant: "destructive" })
      return
    }
    setGenerating(true)
    setGeneratedDescription(null)
    try {
      const res = await fetch(`${API_ENDPOINTS.iMAGE_GENERATOR}generate-text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          keywords: generatedPrompt,
          tone,
          length,
          include_hashtags: includeHashtags
        }),
      })
      const data = await res.json()
      setGeneratedDescription(data.response)
      toast({ title: "Success", description: "Description generated" })
    } catch {
      toast({ title: "Error", description: "Failed to generate description", variant: "destructive" })
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">

      {/* Prompt Builder */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <h2 className="text-lg font-semibold">Prompt Builder</h2>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="brand">Brand Name</Label>
              <Input id="brand" placeholder="Brand..." value={brand} onChange={e => setBrand(e.target.value)} />
            </div>
            <div>
              <Label htmlFor="date">Date</Label>
              <Input id="date" type="date" value={date} onChange={e => setDate(e.target.value)} />
            </div>
          </div>

          <div className="space-y-2">
            <Label>Target Audience</Label>
            <div className="relative">
              <div className="max-h-48 overflow-y-auto rounded-md border bg-popover text-popover-foreground shadow-md p-2 space-y-2">
                {audienceOptions.map((option) => (
                  <label key={option} className="flex items-center space-x-2 p-2 hover:bg-accent rounded cursor-pointer">
                    <input
                      type="checkbox"
                      checked={audience.includes(option)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setAudience([...audience, option]);
                        } else {
                          setAudience(audience.filter(a => a !== option));
                        }
                      }}
                      className="h-4 w-4 rounded border-primary text-primary focus:ring-primary"
                    />
                    <span className="text-sm">{option}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          <div>
            <Label htmlFor="category">Category</Label>
            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger id="category"><SelectValue placeholder="Select"/></SelectTrigger>
              <SelectContent>
                <SelectItem value="Electronics">Electronics</SelectItem>
                <SelectItem value="Fashion">Fashion</SelectItem>
                <SelectItem value="Food">Food</SelectItem>
                <SelectItem value="Beauty">Beauty</SelectItem>
                <SelectItem value="Education">Education</SelectItem>
                {/* ... */}
              </SelectContent>
            </Select>
          </div>

          <div>
            <Label htmlFor="tone">Tone</Label>
            <Select value={tone} onValueChange={setTone}>
              <SelectTrigger id="tone"><SelectValue/></SelectTrigger>
              <SelectContent>
                {toneOptions.map(t => <SelectItem key={t} value={t}>{t}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-center space-x-2">
            <Switch id="cta" checked={includeCTA} onCheckedChange={setIncludeCTA} />
            <Label htmlFor="cta">Include CTA</Label>
          </div>
          {includeCTA && (
            <Input placeholder="e.g. Shop now" value={ctaText} onChange={e => setCtaText(e.target.value)} />
          )}

          <div className="flex items-center space-x-2">
            <Switch id="emojis" checked={includeEmojis} onCheckedChange={setIncludeEmojis} />
            <Label htmlFor="emojis">Include Emojis</Label>
          </div>

          <div>
            <Label htmlFor="language">Language</Label>
            <Select value={language} onValueChange={setLanguage}>
              <SelectTrigger id="language"><SelectValue/></SelectTrigger>
              <SelectContent>
                <SelectItem value="English">English</SelectItem>
                <SelectItem value="French">French</SelectItem>
                <SelectItem value="Arabic">Arabic</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div>
            <Label htmlFor="hashtags">Custom Hashtags</Label>
            <Input id="hashtags" placeholder="#promo #sale" value={hashtagInput} onChange={e => setHashtagInput(e.target.value)} />
          </div>

          <Button onClick={handleGeneratePrompt} className="w-full">Build Prompt</Button>

          {generatedPrompt && (
            <Textarea
              value={generatedPrompt}
              onChange={e => setGeneratedPrompt(e.target.value)}
              className="min-h-24 mt-2"
            />
          )}
        </CardContent>
      </Card>

      {/* Description Generator */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <h2 className="text-lg font-semibold">Description Generator</h2>

          <div>
            <Label htmlFor="length">Length</Label>
            <Select value={length} onValueChange={setLength}>
              <SelectTrigger id="length"><SelectValue/></SelectTrigger>
              <SelectContent>
                <SelectItem value="short">Short (50-75 words)</SelectItem>
                <SelectItem value="medium">Medium (75-150 words)</SelectItem>
                <SelectItem value="long">Long (150-300 words)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-center space-x-2">
            <Switch id="hashtagsDesc" checked={includeHashtags} onCheckedChange={setIncludeHashtags} />
            <Label htmlFor="hashtagsDesc">Include Hashtags</Label>
          </div>

          <Button onClick={handleGenerateDescription} disabled={generating} className="w-full">
            {generating ? 'Generating...' : 'Generate Description'}
          </Button>

          {generatedDescription ? (
            <div className="mt-4 space-y-2">
              <div className="p-4 border rounded bg-muted/30 whitespace-pre-wrap">{generatedDescription}</div>
              <Button variant="outline" size="sm" onClick={() => navigator.clipboard.writeText(generatedDescription)}>Copy</Button>
            </div>
          ) : (
            <div className="text-center p-12 border-2 border-dashed rounded">Use the prompt builder to start</div>
          )}
        </CardContent>
      </Card>

    </div>
  )
}
