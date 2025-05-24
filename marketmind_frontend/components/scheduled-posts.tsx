import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Calendar, Clock, Edit, Facebook, Instagram, Linkedin, MoreHorizontal, Trash, Twitter } from "lucide-react"
import Image from "next/image"

export function ScheduledPosts() {
  const scheduledPosts = [
    {
      id: 1,
      image: "/placeholder.svg?height=300&width=300",
      description: "Exciting news coming soon! Stay tuned for our latest product launch.",
      date: "2023-03-15",
      time: "09:30",
      platforms: ["instagram", "facebook"],
    },
    {
      id: 2,
      image: "/placeholder.svg?height=300&width=300",
      description: "Check out our new blog post on industry trends and insights.",
      date: "2023-03-18",
      time: "14:00",
      platforms: ["twitter", "linkedin"],
    },
    {
      id: 3,
      image: "/placeholder.svg?height=300&width=300",
      description: "Behind the scenes look at our creative process. #BehindTheScenes",
      date: "2023-03-20",
      time: "17:45",
      platforms: ["instagram"],
    },
  ]

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case "instagram":
        return <Instagram className="h-4 w-4" />
      case "facebook":
        return <Facebook className="h-4 w-4" />
      case "twitter":
        return <Twitter className="h-4 w-4" />
      case "linkedin":
        return <Linkedin className="h-4 w-4" />
      default:
        return null
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Scheduled Posts</CardTitle>
        <CardDescription>Manage your upcoming scheduled social media posts</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {scheduledPosts.map((post) => (
            <div key={post.id} className="flex gap-4 p-4 border rounded-lg">
              <div className="relative h-24 w-24 shrink-0 overflow-hidden rounded-md">
                <Image src={post.image || "/placeholder.svg"} alt={`Post ${post.id}`} fill className="object-cover" />
              </div>

              <div className="flex-1 space-y-2">
                <p className="text-sm line-clamp-2">{post.description}</p>

                <div className="flex flex-wrap gap-2">
                  <div className="flex items-center text-xs text-muted-foreground">
                    <Calendar className="h-3 w-3 mr-1" />
                    {post.date}
                  </div>
                  <div className="flex items-center text-xs text-muted-foreground">
                    <Clock className="h-3 w-3 mr-1" />
                    {post.time}
                  </div>
                </div>

                <div className="flex gap-1">
                  {post.platforms.map((platform) => (
                    <Badge key={platform} variant="outline" className="flex items-center gap-1">
                      {getPlatformIcon(platform)}
                      <span className="capitalize">{platform}</span>
                    </Badge>
                  ))}
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <Button variant="ghost" size="icon">
                  <Edit className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon">
                  <Trash className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon">
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

