import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ImageToImageGenerator } from "@/components/image-to-image-generator"

export default function ImageToImageGenerationPage() {
  return (
    <div className="flex flex-col p-6 space-y-6">
      <div className="flex flex-col space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Image-to-Image Transformation</h1>
        <p className="text-muted-foreground">Provide an input image and text prompt to transform your image.</p>
      </div>

      <Tabs defaultValue="transform" className="space-y-4">
        <TabsList>
          <TabsTrigger value="transform">Transform</TabsTrigger>
          <TabsTrigger value="history">History</TabsTrigger>
          <TabsTrigger value="templates">Templates</TabsTrigger>
        </TabsList>
        <TabsContent value="transform" className="space-y-4">
          <ImageToImageGenerator />
        </TabsContent>
        <TabsContent value="history" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Transformation History</CardTitle>
              <CardDescription>View and reuse your previous transformations</CardDescription>
            </CardHeader>
            <CardContent>
              <p>Your transformation history will appear here.</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="templates" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Templates</CardTitle>
              <CardDescription>Use pre-defined templates for quick image transformations</CardDescription>
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