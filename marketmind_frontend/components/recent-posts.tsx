import Image from "next/image"
import { Badge } from "@/components/ui/badge"
import { Heart, MessageSquare, Share2 } from "lucide-react"

export function RecentPosts() {
  const posts = [
    {
      id: 1,
      image: "/placeholder.svg?height=300&width=300",
      platform: "Instagram",
      date: "2 hours ago",
      likes: 245,
      comments: 32,
      shares: 12,
      sentiment: "positive",
    },
    {
      id: 2,
      image: "/placeholder.svg?height=300&width=300",
      platform: "Twitter",
      date: "5 hours ago",
      likes: 124,
      comments: 18,
      shares: 45,
      sentiment: "neutral",
    },
    {
      id: 3,
      image: "/placeholder.svg?height=300&width=300",
      platform: "Facebook",
      date: "1 day ago",
      likes: 532,
      comments: 64,
      shares: 28,
      sentiment: "positive",
    },
  ]

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {posts.map((post) => (
        <div key={post.id} className="border rounded-lg overflow-hidden">
          <div className="relative h-48">
            <Image src={post.image || "/placeholder.svg"} alt={`Post ${post.id}`} fill className="object-cover" />
          </div>
          <div className="p-4">
            <div className="flex justify-between items-center mb-2">
              <Badge variant={post.platform === "Instagram" ? "default" : "outline"}>{post.platform}</Badge>
              <span className="text-xs text-muted-foreground">{post.date}</span>
            </div>
            <div className="flex justify-between mt-4">
              <div className="flex items-center space-x-1">
                <Heart className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">{post.likes}</span>
              </div>
              <div className="flex items-center space-x-1">
                <MessageSquare className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">{post.comments}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Share2 className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">{post.shares}</span>
              </div>
              <Badge
                variant={
                  post.sentiment === "positive" ? "default" : post.sentiment === "neutral" ? "outline" : "destructive"
                }
              >
                {post.sentiment}
              </Badge>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

