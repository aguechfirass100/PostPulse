import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { SocialMediaIntegration } from "@/components/social-media-integration"
import { ScheduledPosts } from "@/components/scheduled-posts"

export default function SocialMediaPage() {
  return (
    <div className="flex flex-col p-6 space-y-6">
      <div className="flex flex-col space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Social Media Integration</h1>
        <p className="text-muted-foreground">Connect, manage, and schedule your social media posts across platforms.</p>
      </div>

      <Tabs defaultValue="post" className="space-y-4">
        <TabsList>
          <TabsTrigger value="post">Create Post</TabsTrigger>
          <TabsTrigger value="scheduled">Scheduled</TabsTrigger>
          <TabsTrigger value="accounts">Connected Accounts</TabsTrigger>
        </TabsList>
        <TabsContent value="post" className="space-y-4">
          <SocialMediaIntegration />
        </TabsContent>
        <TabsContent value="scheduled" className="space-y-4">
          <ScheduledPosts />
        </TabsContent>
        <TabsContent value="accounts" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Connected Accounts</CardTitle>
              <CardDescription>Manage your connected social media accounts</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Your connected accounts will appear here.</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

