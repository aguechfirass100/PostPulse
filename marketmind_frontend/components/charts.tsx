"use client"

import { useEffect, useRef } from "react"

export function LineChart() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (!canvasRef.current) return

    const ctx = canvasRef.current.getContext("2d")
    if (!ctx) return

    // Clear canvas
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height)

    // Set dimensions
    const width = canvasRef.current.width
    const height = canvasRef.current.height
    const padding = 40

    // Sample data
    const data = [15, 25, 35, 45, 35, 55, 45, 60, 75, 70, 65, 80, 85, 80, 90]

    // Draw axes
    ctx.beginPath()
    ctx.moveTo(padding, padding)
    ctx.lineTo(padding, height - padding)
    ctx.lineTo(width - padding, height - padding)
    ctx.strokeStyle = "#d4d4d8"
    ctx.stroke()

    // Draw line
    const xStep = (width - 2 * padding) / (data.length - 1)
    const yMax = Math.max(...data) * 1.1

    ctx.beginPath()
    ctx.moveTo(padding, height - padding - (data[0] / yMax) * (height - 2 * padding))

    for (let i = 1; i < data.length; i++) {
      ctx.lineTo(padding + i * xStep, height - padding - (data[i] / yMax) * (height - 2 * padding))
    }

    ctx.strokeStyle = "hsl(267, 75%, 40%)"
    ctx.lineWidth = 2
    ctx.stroke()

    // Fill area under the line
    ctx.lineTo(padding + (data.length - 1) * xStep, height - padding)
    ctx.lineTo(padding, height - padding)
    ctx.fillStyle = "hsla(267, 75%, 40%, 0.1)"
    ctx.fill()

    // Add points
    for (let i = 0; i < data.length; i++) {
      ctx.beginPath()
      ctx.arc(padding + i * xStep, height - padding - (data[i] / yMax) * (height - 2 * padding), 4, 0, 2 * Math.PI)
      ctx.fillStyle = "hsl(267, 75%, 40%)"
      ctx.fill()
    }
  }, [])

  return <canvas ref={canvasRef} width={500} height={300} className="w-full h-full" />
}

export function BarChart() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (!canvasRef.current) return

    const ctx = canvasRef.current.getContext("2d")
    if (!ctx) return

    // Clear canvas
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height)

    // Set dimensions
    const width = canvasRef.current.width
    const height = canvasRef.current.height
    const padding = 40

    // Sample data
    const data = [65, 45, 75, 35, 95]
    const labels = ["Instagram", "Facebook", "Twitter", "LinkedIn", "TikTok"]

    // Draw axes
    ctx.beginPath()
    ctx.moveTo(padding, padding)
    ctx.lineTo(padding, height - padding)
    ctx.lineTo(width - padding, height - padding)
    ctx.strokeStyle = "#d4d4d8"
    ctx.stroke()

    // Draw bars
    const barWidth = ((width - 2 * padding) / data.length) * 0.8
    const barSpacing = ((width - 2 * padding) / data.length) * 0.2
    const yMax = Math.max(...data) * 1.1

    for (let i = 0; i < data.length; i++) {
      const barHeight = (data[i] / yMax) * (height - 2 * padding)
      const x = padding + i * (barWidth + barSpacing) + barSpacing / 2
      const y = height - padding - barHeight

      ctx.fillStyle = `hsl(${267 + i * 10}, 75%, 40%)`
      ctx.fillRect(x, y, barWidth, barHeight)

      // Add label
      ctx.fillStyle = "#71717a"
      ctx.font = "10px sans-serif"
      ctx.textAlign = "center"
      ctx.fillText(labels[i], x + barWidth / 2, height - padding + 15)
    }
  }, [])

  return <canvas ref={canvasRef} width={500} height={300} className="w-full h-full" />
}

export function PieChart() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (!canvasRef.current) return

    const ctx = canvasRef.current.getContext("2d")
    if (!ctx) return

    // Clear canvas
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height)

    // Set dimensions
    const width = canvasRef.current.width
    const height = canvasRef.current.height
    const centerX = width / 2
    const centerY = height / 2
    const radius = Math.min(width, height) / 2 - 40

    // Sample data
    const data = [35, 25, 20, 15, 5]
    const labels = ["Images", "Videos", "Carousels", "Stories", "Reels"]
    const colors = [
      "hsl(267, 75%, 40%)",
      "hsl(277, 75%, 40%)",
      "hsl(287, 75%, 40%)",
      "hsl(297, 75%, 40%)",
      "hsl(307, 75%, 40%)",
    ]

    // Draw pie
    let startAngle = 0
    const total = data.reduce((sum, value) => sum + value, 0)

    for (let i = 0; i < data.length; i++) {
      const sliceAngle = (2 * Math.PI * data[i]) / total

      ctx.beginPath()
      ctx.moveTo(centerX, centerY)
      ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle)
      ctx.closePath()

      ctx.fillStyle = colors[i]
      ctx.fill()

      // Add label line and text
      const midAngle = startAngle + sliceAngle / 2
      const labelRadius = radius * 1.2
      const labelX = centerX + Math.cos(midAngle) * labelRadius
      const labelY = centerY + Math.sin(midAngle) * labelRadius

      ctx.beginPath()
      ctx.moveTo(centerX + Math.cos(midAngle) * radius, centerY + Math.sin(midAngle) * radius)
      ctx.lineTo(labelX, labelY)
      ctx.strokeStyle = colors[i]
      ctx.stroke()

      ctx.font = "12px sans-serif"
      ctx.fillStyle = "#71717a"
      ctx.textAlign = midAngle < Math.PI ? "left" : "right"
      ctx.fillText(`${labels[i]} (${data[i]}%)`, labelX, labelY)

      startAngle += sliceAngle
    }
  }, [])

  return <canvas ref={canvasRef} width={500} height={300} className="w-full h-full" />
}

