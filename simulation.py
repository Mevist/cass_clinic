import patient_simulation
import time
import threading
from datetime import datetime, timedelta

class Simulation:
    
    def __init__(self) -> None:
        self.time_increment = 3
        self.today = datetime.now()
        self.days = self.today.strftime("%Y-%m-%d")
        self.time_now = self.today.strftime("%H:%M:%S")

        self.time_tick_thread = threading.Thread(target=self.time_tick)
        self.time_tick_event = threading.Event()
        self.time_print_event = threading.Event()

    def print_datetime(self):
        print(self.today)
        print(self.today + timedelta(hours=24))
    
    def split_datetime(self):
        days = self.today.strftime("%Y-%m-%d")
        time_split = self.today.strftime("%H:%M:%S")
        print(days, time_split)

    def time_tick(self):
        while True:
            self.time_tick_event.clear()
            self.time_print_event.clear()
            time.sleep(self.time_increment)
            self.today += timedelta(minutes=30)
            self.time_tick_event.set()
            self.time_print_event.wait()
            

    def time_tick_print(self):
        self.time_tick_event.wait()
        print(self.today)
        self.time_print_event.set()

    def start_simulation(self):
        self.time_tick_thread.start()

    def stop_simulation(self):
        self.time_tick_thread.join()

if __name__ == "__main__":
    simulation_v1 = Simulation()

    simulation_v1.print_datetime()
    simulation_v1.split_datetime()
    simulation_v1.start_simulation()
    print()
    while True:
        simulation_v1.time_tick_print()