import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { DescriptionGenerator } from "@/components/description-generator"

export default function DescriptionGenerationPage() {
  return (
    <div className="flex flex-col p-6 space-y-6">
      <div className="flex flex-col space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Description Generation</h1>
        <p className="text-muted-foreground">Generate engaging descriptions for your social media content.</p>
      </div>

      <Tabs defaultValue="generate" className="space-y-4">
        <TabsList>
          <TabsTrigger value="generate">Generate</TabsTrigger>
          <TabsTrigger value="history">History</TabsTrigger>
          <TabsTrigger value="templates">Templates</TabsTrigger>
        </TabsList>
        <TabsContent value="generate" className="space-y-4">
          <DescriptionGenerator />
        </TabsContent>
        <TabsContent value="history" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Generation History</CardTitle>
              <CardDescription>View and reuse your previously generated descriptions</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Your generation history will appear here.</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="templates" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Templates</CardTitle>
              <CardDescription>Use pre-defined templates for quick description generation</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Templates will appear here.</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

