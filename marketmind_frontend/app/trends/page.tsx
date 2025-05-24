import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { TrendDashboard } from "@/components/trend-dashboard"

export default function TrendsPage() {
  return (
    <div className="flex flex-col p-6 space-y-6">
      <div className="flex flex-col space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Trend Analysis</h1>
        <p className="text-muted-foreground">Track engagement metrics and analyze content performance.</p>
      </div>

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="engagement">Engagement</TabsTrigger>
          <TabsTrigger value="content">Content Performance</TabsTrigger>
          <TabsTrigger value="audience">Audience</TabsTrigger>
        </TabsList>
        <TabsContent value="overview" className="space-y-4">
          <TrendDashboard />
        </TabsContent>
        <TabsContent value="engagement" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Engagement Metrics</CardTitle>
              <CardDescription>Detailed engagement metrics across platforms</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Engagement metrics will appear here.</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="content" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Content Performance</CardTitle>
              <CardDescription>Analyze which content types perform best</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Content performance metrics will appear here.</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="audience" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Audience Insights</CardTitle>
              <CardDescription>Understand your audience demographics and behavior</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Audience insights will appear here.</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

