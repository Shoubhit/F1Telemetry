import fastf1
import asyncio

class RaceState:
    def __init__(self, Date, SessionTime, DriverAhead, DistanceToDriverAhead, Time,
                 RPM, Speed, nGear, Throttle, Brake, DRS, Source,
                 Distance, RelativeDistance, Status, X, Y, Z):
        self.Date = Date
        self.SessionTime = SessionTime 
        self.DriverAhead = DriverAhead
        self.DistanceToDriverAhead = DistanceToDriverAhead
        self.Time = Time
        self.RPM = RPM
        self.Speed = Speed
        self.nGear = nGear
        self.Throttle = Throttle
        self.Brake = Brake
        self.DRS = DRS
        self.Source = Source
        self.Distance = Distance
        self.RelativeDistance = RelativeDistance
        self.Status = Status
        self.X = X
        self.Y = Y
        self.Z = Z

class RaceSimulation:
    def __init__(self, year, grand_prix, session_type, driver, lap=None, playback_speed=1.0):
        self.year = year
        self.grand_prix = grand_prix
        self.lap = lap
        self.session_type = session_type
        self.driver = driver
        self.playback_speed = playback_speed
        self.session = fastf1.get_session(year, grand_prix, session_type)
        self.session.load()
        self.session = self.session.laps.pick_drivers(driver)
        self.lap_data = self.get_lap_data()
        self.lap_data["Time_seconds"] = self.lap_data["Time"].dt.total_seconds()
        self.timestamps = self.lap_data['Time_seconds'].tolist()
        self.race_state = self.set_race_state(0)

    def get_lap_data(self):
        if self.lap is not None:
            return self.session.pick_laps(self.lap).get_telemetry()
        else:
            return self.session.pick_fastest().get_telemetry()
        
    def set_race_state(self, index: int):
        # Set the simulation state to the new race state
        self.race_state = RaceState(
            Date=self.lap_data['Date'].iloc[index],
            SessionTime=self.lap_data['SessionTime'].iloc[index],
            DriverAhead=self.lap_data['DriverAhead'].iloc[index],
            DistanceToDriverAhead=self.lap_data['DistanceToDriverAhead'].iloc[index],
            Time=self.lap_data['Time_seconds'].iloc[index],
            RPM=self.lap_data['RPM'].iloc[index],
            Speed=self.lap_data['Speed'].iloc[index],
            nGear=self.lap_data['nGear'].iloc[index],
            Throttle=self.lap_data['Throttle'].iloc[index],
            Brake=self.lap_data['Brake'].iloc[index],
            DRS=self.lap_data['DRS'].iloc[index],
            Source=self.lap_data['Source'].iloc[index],
            Distance=self.lap_data['Distance'].iloc[index],
            RelativeDistance=self.lap_data['RelativeDistance'].iloc[index],
            Status=self.lap_data['Status'].iloc[index],
            X=self.lap_data['X'].iloc[index],
            Y=self.lap_data['Y'].iloc[index],
            Z=self.lap_data['Z'].iloc[index]
        )

    async def run_sim(self):
        for i in range(len(self.timestamps) - 1):
            current_time = self.timestamps[i]
            next_time = self.timestamps[i + 1]

            self.set_race_state(i)

            # Wait real time difference between this and the next frame (scaled)
            delay = (next_time - current_time) / self.playback_speed
            print(f"Simulating time: {current_time} seconds, Driver: {self.driver}, Speed: {self.lap_data['Speed'].iloc[i]} km/h, Position: ({self.lap_data['X'].iloc[i]}, {self.lap_data['Y'].iloc[i]})")
            await asyncio.sleep(delay)


sim = RaceSimulation(2023, 'Monza', 'R', 'VER')

asyncio.run(sim.run_sim())