'use client'

import { useState, useEffect } from 'react'
import DriverList from '../components/DriverList'
import RaceMap from '../components/RaceMap'
import TelemetryChart from '../components/TelemetryChart'
import ControlPanel from '../components/ControlPanel'

interface TelemetryData {
  driver_id: string
  driver_name: string
  timestamp: string
  speed: number
  throttle: number
  brake: number
  gear: number
  rpm: number
  position: number
  lap_number: number
  coordinates?: { x: number; y: number; z: number }
}

interface Driver {
  driver_id: string
  driver_name: string
  car_number: string
  team: string
}

export default function Home() {
  const [drivers, setDrivers] = useState<Driver[]>([])
  const [selectedDriver, setSelectedDriver] = useState<string>('VER')
  const [telemetryData, setTelemetryData] = useState<TelemetryData[]>([])
  const [isConnected, setIsConnected] = useState(false)
  const [ws, setWs] = useState<WebSocket | null>(null)

  // WebSocket connection
  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8765')
    
    websocket.onopen = () => {
      console.log('WebSocket connected')
      setIsConnected(true)
    }
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'telemetry') {
        setTelemetryData(prev => [data.data, ...prev.slice(0, 99)]) // Keep last 100 points
      }
    }
    
    websocket.onclose = () => {
      console.log('WebSocket disconnected')
      setIsConnected(false)
    }
    
    setWs(websocket)
    
    return () => {
      websocket.close()
    }
  }, [])

  // Fetch drivers from API
  useEffect(() => {
    const fetchDrivers = async () => {
      try {
        const response = await fetch('http://localhost:8000/drivers')
        if (response.ok) {
          const data = await response.json()
          setDrivers(data)
        }
      } catch (error) {
        console.error('Failed to fetch drivers:', error)
      }
    }
    
    fetchDrivers()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="f1-gradient text-white p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl font-bold">🏎️ F1 Telemetry Dashboard</h1>
          <p className="text-xl mt-2">Real-time Formula 1 telemetry visualization</p>
          <div className="flex items-center mt-4">
            <div className={`w-3 h-3 rounded-full mr-2 ${isConnected ? 'bg-green-400' : 'bg-red-400'}`}></div>
            <span className="text-sm">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Controls and Driver List */}
          <div className="space-y-6">
            <ControlPanel />
            <DriverList 
              drivers={drivers}
              selectedDriver={selectedDriver}
              onDriverSelect={setSelectedDriver}
            />
          </div>

          {/* Center Column - Race Map */}
          <div className="lg:col-span-2">
            <div className="f1-card">
              <h2 className="text-2xl font-bold mb-4">Race Map</h2>
              <RaceMap 
                telemetryData={telemetryData.filter(t => t.driver_id === selectedDriver)}
                selectedDriver={selectedDriver}
              />
            </div>
          </div>
        </div>

        {/* Bottom Row - Telemetry Charts */}
        <div className="mt-6">
          <div className="f1-card">
            <h2 className="text-2xl font-bold mb-4">Telemetry Data</h2>
            <TelemetryChart 
              telemetryData={telemetryData.filter(t => t.driver_id === selectedDriver)}
              selectedDriver={selectedDriver}
            />
          </div>
        </div>
      </main>
    </div>
  )
} 