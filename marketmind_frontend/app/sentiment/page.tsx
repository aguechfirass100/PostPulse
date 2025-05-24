import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { SentimentAnalysis } from "@/components/sentiment-analysis"

export default function SentimentPage() {
  return (
    <div className="flex flex-col p-6 space-y-6">
      <div className="flex flex-col space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Sentiment Analysis</h1>
        <p className="text-muted-foreground">
          Analyze the sentiment of comments and feedback across your social media.
        </p>
      </div>

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="comments">Comments</TabsTrigger>
          <TabsTrigger value="trends">Sentiment Trends</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
        </TabsList>
        <TabsContent value="overview" className="space-y-4">
          <SentimentAnalysis />
        </TabsContent>
        <TabsContent value="comments" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Comment Analysis</CardTitle>
              <CardDescription>Detailed analysis of individual comments</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Comment analysis will appear here.</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="trends" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Sentiment Trends</CardTitle>
              <CardDescription>Track sentiment changes over time</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Sentiment trends will appear here.</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="reports" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Sentiment Reports</CardTitle>
              <CardDescription>Generate and download sentiment analysis reports</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Sentiment reports will appear here.</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

