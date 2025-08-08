'use client'

import { useState } from 'react'

interface ControlPanelProps {}

export default function ControlPanel({}: ControlPanelProps) {
  const [isRunning, setIsRunning] = useState(false)
  const [selectedDriver, setSelectedDriver] = useState('VER')
  const [playbackSpeed, setPlaybackSpeed] = useState(1.0)

  const handleStart = async () => {
    try {
      const response = await fetch('http://localhost:8000/control', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'start',
          driver_id: selectedDriver,
          playback_speed: playbackSpeed,
        }),
      })
      
      if (response.ok) {
        setIsRunning(true)
      }
    } catch (error) {
      console.error('Failed to start simulation:', error)
    }
  }

  const handleStop = async () => {
    try {
      const response = await fetch('http://localhost:8000/control', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'stop',
        }),
      })
      
      if (response.ok) {
        setIsRunning(false)
      }
    } catch (error) {
      console.error('Failed to stop simulation:', error)
    }
  }

  return (
    <div className="f1-card">
      <h2 className="text-xl font-bold mb-4">Control Panel</h2>
      
      <div className="space-y-4">
        {/* Driver Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Driver
          </label>
          <select
            value={selectedDriver}
            onChange={(e) => setSelectedDriver(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-f1-red focus:border-transparent"
          >
            <option value="VER">Max Verstappen</option>
            <option value="HAM">Lewis Hamilton</option>
            <option value="PER">Sergio Pérez</option>
            <option value="LEC">Charles Leclerc</option>
            <option value="SAI">Carlos Sainz</option>
          </select>
        </div>

        {/* Playback Speed */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Playback Speed: {playbackSpeed}x
          </label>
          <input
            type="range"
            min="0.1"
            max="5"
            step="0.1"
            value={playbackSpeed}
            onChange={(e) => setPlaybackSpeed(parseFloat(e.target.value))}
            className="w-full"
          />
        </div>

        {/* Control Buttons */}
        <div className="flex space-x-2">
          <button
            onClick={handleStart}
            disabled={isRunning}
            className="f1-button disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isRunning ? 'Running...' : 'Start Simulation'}
          </button>
          
          <button
            onClick={handleStop}
            disabled={!isRunning}
            className="f1-button-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Stop
          </button>
        </div>

        {/* Status */}
        <div className="text-sm text-gray-600">
          <div className="flex items-center">
            <div className={`w-2 h-2 rounded-full mr-2 ${isRunning ? 'bg-green-400' : 'bg-gray-400'}`}></div>
            Status: {isRunning ? 'Running' : 'Stopped'}
          </div>
        </div>
      </div>
    </div>
  )
} 