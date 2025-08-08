'use client'

interface Driver {
  driver_id: string
  driver_name: string
  car_number: string
  team: string
}

interface DriverListProps {
  drivers: Driver[]
  selectedDriver: string
  onDriverSelect: (driverId: string) => void
}

export default function DriverList({ drivers, selectedDriver, onDriverSelect }: DriverListProps) {
  const getTeamColor = (team: string) => {
    const teamColors: { [key: string]: string } = {
      'Red Bull Racing': 'bg-red-500',
      'Mercedes': 'bg-teal-500',
      'Ferrari': 'bg-red-600',
      'McLaren': 'bg-orange-500',
      'Aston Martin': 'bg-green-500',
      'Alpine': 'bg-blue-500',
      'Williams': 'bg-blue-600',
      'AlphaTauri': 'bg-blue-700',
      'Alfa Romeo': 'bg-red-700',
      'Haas F1 Team': 'bg-gray-500',
    }
    return teamColors[team] || 'bg-gray-400'
  }

  return (
    <div className="f1-card">
      <h2 className="text-xl font-bold mb-4">Drivers</h2>
      
      {drivers.length === 0 ? (
        <div className="text-gray-500 text-center py-8">
          <p>No drivers available</p>
          <p className="text-sm">Start the simulation to load drivers</p>
        </div>
      ) : (
        <div className="space-y-2">
          {drivers.map((driver) => (
            <div
              key={driver.driver_id}
              onClick={() => onDriverSelect(driver.driver_id)}
              className={`p-3 rounded-lg cursor-pointer transition-colors duration-200 ${
                selectedDriver === driver.driver_id
                  ? 'bg-f1-red text-white'
                  : 'bg-gray-100 hover:bg-gray-200'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className={`w-3 h-3 rounded-full ${getTeamColor(driver.team)}`}></div>
                  <div>
                    <div className="font-semibold">{driver.driver_name}</div>
                    <div className="text-sm opacity-75">{driver.team}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-lg">#{driver.car_number}</div>
                  <div className="text-xs opacity-75">{driver.driver_id}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
} 