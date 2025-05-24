import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowUp, ArrowDown, Users, Eye, ThumbsUp, MessageSquare } from "lucide-react"

export function EngagementStats() {
  return (
    <>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Followers</CardTitle>
          <Users className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">12,543</div>
          <p className="text-xs text-muted-foreground flex items-center">
            <ArrowUp className="mr-1 h-4 w-4 text-green-500" />
            <span className="text-green-500 font-medium">+12.5%</span> from last month
          </p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Impressions</CardTitle>
          <Eye className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">245.7K</div>
          <p className="text-xs text-muted-foreground flex items-center">
            <ArrowUp className="mr-1 h-4 w-4 text-green-500" />
            <span className="text-green-500 font-medium">+18.2%</span> from last month
          </p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Engagement Rate</CardTitle>
          <ThumbsUp className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">4.3%</div>
          <p className="text-xs text-muted-foreground flex items-center">
            <ArrowDown className="mr-1 h-4 w-4 text-red-500" />
            <span className="text-red-500 font-medium">-0.5%</span> from last month
          </p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Comments</CardTitle>
          <MessageSquare className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">1,324</div>
          <p className="text-xs text-muted-foreground flex items-center">
            <ArrowUp className="mr-1 h-4 w-4 text-green-500" />
            <span className="text-green-500 font-medium">+8.1%</span> from last month
          </p>
        </CardContent>
      </Card>
    </>
  )
}

