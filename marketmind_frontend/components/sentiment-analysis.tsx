"use client"

import { useState } from "react"
import Image from "next/image"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { AlertTriangle, Flag, MessageSquare, ThumbsUp } from "lucide-react"
import { Progress } from "@/components/ui/progress"

export function SentimentAnalysis() {
  const [selectedPost, setSelectedPost] = useState("1")

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4">
        <Select value={selectedPost} onValueChange={setSelectedPost}>
          <SelectTrigger className="w-[300px]">
            <SelectValue placeholder="Select post to analyze" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="1">Product Launch Announcement (Instagram)</SelectItem>
            <SelectItem value="2">Behind the Scenes Video (Facebook)</SelectItem>
            <SelectItem value="3">Industry News Update (Twitter)</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Selected Post</CardTitle>
            <CardDescription>View the post and its sentiment overview</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4">
              <div className="relative h-32 w-32 shrink-0 overflow-hidden rounded-md">
                <Image src="/placeholder.svg?height=300&width=300" alt="Selected post" fill className="object-cover" />
              </div>

              <div className="flex-1">
                <Badge>Instagram</Badge>
                <h3 className="text-lg font-medium mt-2">Product Launch Announcement</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Excited to announce our new product line! Check out these amazing features that will revolutionize
                  your workflow.
                </p>

                <div className="flex gap-4 mt-4">
                  <div className="flex items-center gap-1">
                    <ThumbsUp className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm">1.2K</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <MessageSquare className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm">87</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Sentiment Overview</CardTitle>
            <CardDescription>Overall sentiment of comments</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="flex items-center">
                    <Badge className="bg-green-500 hover:bg-green-500/90 mr-2">Positive</Badge>
                    72%
                  </span>
                  <span>54 comments</span>
                </div>
                <Progress value={72} className="h-2 bg-muted" />
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="flex items-center">
                    <Badge variant="outline" className="mr-2">
                      Neutral
                    </Badge>
                    18%
                  </span>
                  <span>16 comments</span>
                </div>
                <Progress value={18} className="h-2 bg-muted" />
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="flex items-center">
                    <Badge variant="destructive" className="mr-2">
                      Negative
                    </Badge>
                    10%
                  </span>
                  <span>7 comments</span>
                </div>
                <Progress value={10} className="h-2 bg-muted" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Comment Analysis</CardTitle>
          <CardDescription>Sentiment breakdown of individual comments</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <Alert className="border-green-500/50 bg-green-500/10">
              <ThumbsUp className="h-4 w-4 text-green-500" />
              <AlertTitle className="flex items-center gap-2">
                Positive Comment
                <Badge className="bg-green-500 hover:bg-green-500/90">95% Positive</Badge>
              </AlertTitle>
              <AlertDescription className="mt-2">
                "This is exactly what I've been waiting for! The features look amazing and I can't wait to try it out.
                Great job team!"
              </AlertDescription>
              <div className="flex justify-between items-center mt-2 text-sm text-muted-foreground">
                <span>@happy_user • 2 hours ago</span>
                <Button variant="ghost" size="sm">
                  <Flag className="h-4 w-4 mr-1" />
                  Flag
                </Button>
              </div>
            </Alert>

            <Alert>
              <MessageSquare className="h-4 w-4" />
              <AlertTitle className="flex items-center gap-2">
                Neutral Comment
                <Badge variant="outline">68% Neutral</Badge>
              </AlertTitle>
              <AlertDescription className="mt-2">
                "Interesting product. How does the pricing compare to your previous offerings? Will there be an upgrade
                path for existing customers?"
              </AlertDescription>
              <div className="flex justify-between items-center mt-2 text-sm text-muted-foreground">
                <span>@curious_customer • 5 hours ago</span>
                <Button variant="ghost" size="sm">
                  <Flag className="h-4 w-4 mr-1" />
                  Flag
                </Button>
              </div>
            </Alert>

            <Alert variant="destructive">
              <AlertTriangle className="h-4 w-4" />
              <AlertTitle className="flex items-center gap-2">
                Negative Comment
                <Badge variant="destructive">87% Negative</Badge>
              </AlertTitle>
              <AlertDescription className="mt-2">
                "Disappointed with the lack of Android support. When will you stop ignoring a huge portion of your
                potential customers?"
              </AlertDescription>
              <div className="flex justify-between items-center mt-2 text-sm">
                <span>@frustrated_user • 1 day ago</span>
                <Button variant="ghost" size="sm" className="text-destructive-foreground">
                  <Flag className="h-4 w-4 mr-1" />
                  Flag
                </Button>
              </div>
            </Alert>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

