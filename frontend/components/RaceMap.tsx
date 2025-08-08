'use client'

import { useEffect, useRef } from 'react'

interface TelemetryData {
  coordinates?: { x: number; y: number; z: number }
  speed: number
  timestamp: string
}

interface RaceMapProps {
  telemetryData: TelemetryData[]
  selectedDriver: string
}

export default function RaceMap({ telemetryData, selectedDriver }: RaceMapProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Draw track outline (simplified F1 track)
    ctx.strokeStyle = '#374151'
    ctx.lineWidth = 3
    ctx.beginPath()
    ctx.ellipse(200, 150, 120, 80, 0, 0, 2 * Math.PI)
    ctx.stroke()

    // Draw telemetry points
    if (telemetryData.length > 0) {
      telemetryData.forEach((point, index) => {
        if (point.coordinates) {
          const x = 200 + (point.coordinates.x * 100)
          const y = 150 + (point.coordinates.y * 100)
          
          // Color based on speed
          const speedRatio = point.speed / 300 // Assuming max speed of 300 km/h
          const red = Math.min(255, speedRatio * 255)
          const green = Math.max(0, 255 - speedRatio * 255)
          
          ctx.fillStyle = `rgb(${red}, ${green}, 0)`
          ctx.beginPath()
          ctx.arc(x, y, 3, 0, 2 * Math.PI)
          ctx.fill()
        }
      })
    }

    // Draw driver position
    if (telemetryData.length > 0) {
      const latest = telemetryData[0]
      if (latest.coordinates) {
        const x = 200 + (latest.coordinates.x * 100)
        const y = 150 + (latest.coordinates.y * 100)
        
        ctx.fillStyle = '#E10600'
        ctx.beginPath()
        ctx.arc(x, y, 8, 0, 2 * Math.PI)
        ctx.fill()
        
        ctx.fillStyle = 'white'
        ctx.font = '12px Arial'
        ctx.fillText(selectedDriver, x + 10, y)
      }
    }
  }, [telemetryData, selectedDriver])

  return (
    <div className="relative">
      <canvas
        ref={canvasRef}
        width={400}
        height={300}
        className="border border-gray-300 rounded-lg"
      />
      <div className="mt-2 text-sm text-gray-600">
        <p>Driver: {selectedDriver}</p>
        <p>Data Points: {telemetryData.length}</p>
        {telemetryData.length > 0 && (
          <p>Latest Speed: {telemetryData[0].speed.toFixed(1)} km/h</p>
        )}
      </div>
    </div>
  )
} 