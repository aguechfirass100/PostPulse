"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { BarChart, LineChart } from "@/components/charts"
import { Button } from "@/components/ui/button"
import { Calendar, Download } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import Image from "next/image"

export function TrendDashboard() {
  const [timeRange, setTimeRange] = useState("30days")

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select time range" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7days">Last 7 days</SelectItem>
              <SelectItem value="30days">Last 30 days</SelectItem>
              <SelectItem value="90days">Last 90 days</SelectItem>
              <SelectItem value="year">Last year</SelectItem>
            </SelectContent>
          </Select>

          <Button variant="outline" size="sm" className="flex items-center gap-1">
            <Calendar className="h-4 w-4" />
            Custom Range
          </Button>
        </div>

        <Button variant="outline" size="sm" className="flex items-center gap-1">
          <Download className="h-4 w-4" />
          Export Data
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <MetricCard title="Total Engagement" value="24,521" change="+12.5%" trend="up" />
        <MetricCard title="Avg. Engagement Rate" value="4.8%" change="+0.7%" trend="up" />
        <MetricCard title="Reach" value="142.3K" change="-3.2%" trend="down" />
        <MetricCard title="Follower Growth" value="1,254" change="+8.1%" trend="up" />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Engagement Over Time</CardTitle>
            <CardDescription>Track engagement trends across the selected time period</CardDescription>
          </CardHeader>
          <CardContent className="h-80">
            <LineChart />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Platform Breakdown</CardTitle>
            <CardDescription>Engagement distribution across social platforms</CardDescription>
          </CardHeader>
          <CardContent className="h-80">
            <BarChart />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Top Performing Content</CardTitle>
          <CardDescription>Your best performing posts during this period</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[1, 2, 3].map((id) => (
              <div key={id} className="flex gap-4 p-4 border rounded-lg">
                <div className="relative h-20 w-20 shrink-0 overflow-hidden rounded-md">
                  <Image
                    src={`/placeholder.svg?height=200&width=200`}
                    alt={`Top post ${id}`}
                    fill
                    className="object-cover"
                  />
                </div>

                <div className="flex-1">
                  <div className="flex justify-between items-start">
                    <div>
                      <Badge variant="outline" className="mb-2">
                        Instagram
                      </Badge>
                      <p className="text-sm line-clamp-2">
                        {id === 1
                          ? "Exciting product announcement with behind-the-scenes footage"
                          : id === 2
                            ? "Customer testimonial featuring our latest service"
                            : "Team celebration of our recent industry award"}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium">
                        {id === 1 ? "2,453" : id === 2 ? "1,872" : "1,654"} engagements
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {id === 1 ? "8.2%" : id === 2 ? "7.5%" : "6.9%"} engagement rate
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

function MetricCard({
  title,
  value,
  change,
  trend,
}: {
  title: string
  value: string
  change: string
  trend: "up" | "down"
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className="text-xs text-muted-foreground flex items-center">
          <span className={trend === "up" ? "text-green-500" : "text-red-500"}>{change}</span>
          <span className="ml-1">from previous period</span>
        </p>
      </CardContent>
    </Card>
  )
}

