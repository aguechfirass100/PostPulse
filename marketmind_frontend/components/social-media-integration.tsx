"use client"

import { useState } from "react"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Calendar, Clock, Facebook, Instagram, Linkedin, Twitter, Upload } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"

export function SocialMediaIntegration() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null)
  const [description, setDescription] = useState("")

  const handleImageUpload = () => {
    // Simulate image upload
    setSelectedImage("/placeholder.svg?height=512&width=512")
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Card>
        <CardContent className="p-6">
          <div className="space-y-4">
            <div className="space-y-2">
              <Label>Upload Media</Label>
              <div
                className="border-2 border-dashed rounded-lg p-12 text-center cursor-pointer hover:bg-muted/50 transition-colors"
                onClick={handleImageUpload}
              >
                {selectedImage ? (
                  <div className="relative aspect-square w-full max-w-xs mx-auto overflow-hidden rounded-lg">
                    <Image
                      src={selectedImage || "/placeholder.svg"}
                      alt="Uploaded image"
                      fill
                      className="object-cover"
                    />
                  </div>
                ) : (
                  <div className="space-y-2">
                    <Upload className="h-8 w-8 mx-auto text-muted-foreground" />
                    <p className="text-sm text-muted-foreground">Click to upload an image or video</p>
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Post Description</Label>
              <Textarea
                id="description"
                placeholder="Write your post description..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="min-h-32"
              />
            </div>

            <div className="space-y-2">
              <Label>Select Platforms</Label>
              <div className="flex flex-wrap gap-2">
                <div className="flex items-center space-x-2">
                  <Checkbox id="instagram" defaultChecked />
                  <Label htmlFor="instagram" className="flex items-center">
                    <Instagram className="h-4 w-4 mr-1" />
                    Instagram
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox id="facebook" defaultChecked />
                  <Label htmlFor="facebook" className="flex items-center">
                    <Facebook className="h-4 w-4 mr-1" />
                    Facebook
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox id="twitter" />
                  <Label htmlFor="twitter" className="flex items-center">
                    <Twitter className="h-4 w-4 mr-1" />
                    Twitter
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox id="linkedin" />
                  <Label htmlFor="linkedin" className="flex items-center">
                    <Linkedin className="h-4 w-4 mr-1" />
                    LinkedIn
                  </Label>
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <Label>Schedule</Label>
              <div className="flex gap-2">
                <div className="flex-1 relative">
                  <Input type="date" className="pl-10" />
                  <Calendar className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                </div>
                <div className="flex-1 relative">
                  <Input type="time" className="pl-10" />
                  <Clock className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                </div>
              </div>
            </div>

            <div className="flex gap-2">
              <Button className="flex-1">Post Now</Button>
              <Button variant="outline" className="flex-1">
                Schedule
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-6">
          <Tabs defaultValue="instagram">
            <TabsList className="grid grid-cols-3 mb-4">
              <TabsTrigger value="instagram" className="flex items-center">
                <Instagram className="h-4 w-4 mr-2" />
                Instagram
              </TabsTrigger>
              <TabsTrigger value="facebook" className="flex items-center">
                <Facebook className="h-4 w-4 mr-2" />
                Facebook
              </TabsTrigger>
              <TabsTrigger value="twitter" className="flex items-center">
                <Twitter className="h-4 w-4 mr-2" />
                Twitter
              </TabsTrigger>
            </TabsList>

            <TabsContent value="instagram" className="mt-0">
              <div className="border rounded-lg overflow-hidden bg-white">
                <div className="p-3 border-b flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-primary"></div>
                  <span className="text-sm font-medium">your_account</span>
                </div>

                {selectedImage ? (
                  <div className="relative aspect-square w-full">
                    <Image src={selectedImage || "/placeholder.svg"} alt="Preview" fill className="object-cover" />
                  </div>
                ) : (
                  <div className="aspect-square w-full bg-muted flex items-center justify-center">
                    <p className="text-muted-foreground">Image Preview</p>
                  </div>
                )}

                <div className="p-3">
                  <p className="text-sm">
                    <span className="font-medium">your_account</span> {description || "Your caption will appear here"}
                  </p>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="facebook" className="mt-0">
              <div className="border rounded-lg overflow-hidden bg-white">
                <div className="p-3 border-b flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-primary"></div>
                  <div>
                    <span className="text-sm font-medium block">Your Name</span>
                    <span className="text-xs text-muted-foreground">Just now</span>
                  </div>
                </div>

                <div className="p-3">
                  <p className="text-sm mb-3">{description || "Your post text will appear here"}</p>

                  {selectedImage ? (
                    <div className="relative w-full h-48 rounded overflow-hidden">
                      <Image src={selectedImage || "/placeholder.svg"} alt="Preview" fill className="object-cover" />
                    </div>
                  ) : (
                    <div className="w-full h-48 bg-muted rounded flex items-center justify-center">
                      <p className="text-muted-foreground">Image Preview</p>
                    </div>
                  )}
                </div>
              </div>
            </TabsContent>

            <TabsContent value="twitter" className="mt-0">
              <div className="border rounded-lg overflow-hidden bg-white">
                <div className="p-3 flex gap-2">
                  <div className="w-10 h-10 rounded-full bg-primary shrink-0"></div>
                  <div className="flex-1">
                    <div className="flex items-center gap-1">
                      <span className="text-sm font-medium">Your Name</span>
                      <span className="text-xs text-muted-foreground">@your_handle</span>
                    </div>
                    <p className="text-sm mt-1">{description || "Your tweet will appear here"}</p>

                    {selectedImage && (
                      <div className="relative w-full h-48 mt-2 rounded-lg overflow-hidden">
                        <Image src={selectedImage || "/placeholder.svg"} alt="Preview" fill className="object-cover" />
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}

