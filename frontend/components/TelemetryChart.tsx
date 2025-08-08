'use client'

interface TelemetryData {
  speed: number
  throttle: number
  brake: number
  gear: number
  rpm: number
  timestamp: string
}

interface TelemetryChartProps {
  telemetryData: TelemetryData[]
  selectedDriver: string
}

export default function TelemetryChart({ telemetryData, selectedDriver }: TelemetryChartProps) {
  if (telemetryData.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No telemetry data available</p>
        <p className="text-sm">Start the simulation to see real-time data</p>
      </div>
    )
  }

  const latest = telemetryData[0]

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {/* Speed */}
      <div className="bg-blue-50 p-4 rounded-lg">
        <h3 className="text-sm font-medium text-blue-800">Speed</h3>
        <p className="text-2xl font-bold text-blue-900">
          {latest.speed.toFixed(1)} km/h
        </p>
      </div>

      {/* Throttle */}
      <div className="bg-green-50 p-4 rounded-lg">
        <h3 className="text-sm font-medium text-green-800">Throttle</h3>
        <p className="text-2xl font-bold text-green-900">
          {(latest.throttle * 100).toFixed(1)}%
        </p>
      </div>

      {/* Brake */}
      <div className="bg-red-50 p-4 rounded-lg">
        <h3 className="text-sm font-medium text-red-800">Brake</h3>
        <p className="text-2xl font-bold text-red-900">
          {(latest.brake * 100).toFixed(1)}%
        </p>
      </div>

      {/* Gear */}
      <div className="bg-purple-50 p-4 rounded-lg">
        <h3 className="text-sm font-medium text-purple-800">Gear</h3>
        <p className="text-2xl font-bold text-purple-900">
          {latest.gear}
        </p>
      </div>

      {/* RPM */}
      <div className="bg-orange-50 p-4 rounded-lg">
        <h3 className="text-sm font-medium text-orange-800">RPM</h3>
        <p className="text-2xl font-bold text-orange-900">
          {latest.rpm.toLocaleString()}
        </p>
      </div>

      {/* Driver */}
      <div className="bg-gray-50 p-4 rounded-lg">
        <h3 className="text-sm font-medium text-gray-800">Driver</h3>
        <p className="text-2xl font-bold text-gray-900">
          {selectedDriver}
        </p>
      </div>

      {/* Data Points */}
      <div className="bg-indigo-50 p-4 rounded-lg">
        <h3 className="text-sm font-medium text-indigo-800">Data Points</h3>
        <p className="text-2xl font-bold text-indigo-900">
          {telemetryData.length}
        </p>
      </div>

      {/* Latest Time */}
      <div className="bg-yellow-50 p-4 rounded-lg">
        <h3 className="text-sm font-medium text-yellow-800">Latest</h3>
        <p className="text-sm font-bold text-yellow-900">
          {new Date(latest.timestamp).toLocaleTimeString()}
        </p>
      </div>
    </div>
  )
} 