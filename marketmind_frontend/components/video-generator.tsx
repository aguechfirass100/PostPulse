"use client"

import React, { useState, ChangeEvent } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { toast } from '@/components/ui/use-toast'
import { API_ENDPOINTS } from '@/config/apiEndpoints'
import Image from 'next/image'

export function VideoGenerator() {
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [generatedGif, setGeneratedGif] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(false)

  const handleImageChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null
    setImageFile(file)
    setGeneratedGif(null)
    if (file) {
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
    } else {
      setPreviewUrl(null)
    }
  }

  const handleGenerateGif = async () => {
    if (!imageFile) {
      toast({ title: 'Error', description: 'Please upload an image first', variant: 'destructive' })
      return
    }
    setLoading(true)
    setGeneratedGif(null)
    try {
      const formData = new FormData()
      formData.append('image', imageFile)

      const res = await fetch(`${API_ENDPOINTS.VIDEO_GENERATOR}/generate-video`, {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) throw new Error('Network response was not ok')
      const blob = await res.blob()
      const gifUrl = URL.createObjectURL(blob)
      setGeneratedGif(gifUrl)
      toast({ title: 'Success', description: 'GIF generated successfully' })
    } catch (error) {
      console.error(error)
      toast({ title: 'Error', description: 'Failed to generate GIF', variant: 'destructive' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card>
      <CardContent className="p-6 space-y-4">
        <h2 className="text-lg font-semibold">Video (GIF) Generator</h2>

        <div>
          <Label>Upload Image</Label>
          {previewUrl ? (
            <div className="relative w-full h-64 border rounded-lg overflow-hidden">
              <Image src={previewUrl} alt="Preview" fill className="object-cover" />
              <button
                onClick={() => {
                  setImageFile(null)
                  setPreviewUrl(null)
                }}
                className="absolute top-2 right-2 bg-white rounded-full p-1 shadow"
              >
                ✕
              </button>
            </div>
          ) : (
            <label className="block w-full h-64 border-2 border-dashed border-muted-foreground rounded-lg flex flex-col items-center justify-center cursor-pointer hover:border-primary">
              <input
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleImageChange}
              />
              <span className="text-muted-foreground">Click or drag to upload an image</span>
            </label>
          )}
        </div>

        <Button
          onClick={handleGenerateGif}
          disabled={loading}
          className="w-full"
        >{loading ? 'Generating...' : 'Generate GIF'}</Button>

        {generatedGif && (
          <div>
            <Label>Generated GIF:</Label>
            <img src={generatedGif} alt="Generated GIF" className="mt-2 rounded max-w-full" />
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigator.clipboard.writeText(generatedGif)}
              className="mt-2"
            >Copy URL</Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}