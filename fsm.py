from datetime import datetime
from rs485 import *
from timer import *
import json

PHYSIC = False


import time

class FarmScheduler():
    def __init__(self, debug=True):
        self.debug = debug
        self.schedules = []
        self.current_schedule = None
        self.current_state = IdleState(debug=self.debug)

    def run(self):
        while True:
            if not self.current_schedule:
                self.current_schedule = self.check_schedule()
                if not self.current_schedule:
                    time.sleep(1)  # Sleep briefly to avoid busy waiting
                    continue

            self.current_state = self.current_state.execute(self.current_schedule)
            if isinstance(self.current_state, IdleState) and self.current_schedule['next-cycle'] <= 0:
                print("Cycle complete, checking for new schedules.")
                self.current_schedule = None

            time.sleep(1)  # Main loop tick rate

    def add_schedule(self, schedule):
        self.schedules.append(schedule)

    def check_schedule(self):
        # This is a placeholder for actual schedule checking logic
        for schedule in self.schedules:
            return schedule
        return None

class State:
    def __init__(self, debug=True):
        self.debug = debug

    def execute(self, schedule):
        raise NotImplementedError

    def wait_for_timer(self, timer_id):
        while timer_counters[timer_id] > 0:
            timerRun()
            time.sleep(1)  # Sleep to simulate time passing

class IdleState(State):
    def execute(self, schedule):
        if self.debug:
            print("IDLE STATE")
        if schedule['next-cycle'] > 0:
            return Mixer1State(debug=self.debug)
        else:
            print("FINISHED !!!")
            return self

class Mixer1State(State):
    def execute(self, schedule):
        setTimer(0, int(schedule['mixer1']))
        self.wait_for_timer(0)
        if self.debug:
            print("MIXER1 STATE - Complete")
        return Mixer2State(debug=self.debug)

class Mixer2State(State):
    def execute(self, schedule):
        setTimer(0, int(schedule['mixer2']))
        self.wait_for_timer(0)
        if self.debug:
            print("MIXER2 STATE - Complete")
        return Mixer3State(debug=self.debug)

class Mixer3State(State):
    def execute(self, schedule):
        setTimer(0, int(schedule['mixer3']))
        self.wait_for_timer(0)
        if self.debug:
            print("MIXER3 STATE - Complete")
        return PumpInState(debug=self.debug)

class PumpInState(State):
    def execute(self, schedule):
        setTimer(0, int(schedule['pump-in']))
        self.wait_for_timer(0)
        if self.debug:
            print("PUMP IN STATE - Complete")
        return PumpOutState(debug=self.debug)

class PumpOutState(State):
    def execute(self, schedule):
        setTimer(0, int(schedule['pump-out']))
        self.wait_for_timer(0)
        if self.debug:
            print("PUMP OUT STATE - Complete")
        return IdleState(debug=self.debug)



def convert_schedule_json_to_dict(json_data):
    return json.loads(json_data)


if __name__ == '__main__':
    sched1 = FarmScheduler()
    mqtt_json_data_t1 = '{"mixer1": 3, "mixer2": 3, "mixer3": 3, "pump_in": 3, "pump_out": 3, "selector": "A", "cycle": 2, "startTime": "16:43"}'
    mqtt_json_data_t2 = '{"mixer1": 3, "mixer2": 3, "mixer3": 3, "pump_in": 3, "pump_out": 3, "selector": "A", "cycle": 2, "startTime": "15:30"}'

    sched1.add_schedule(convert_schedule_json_to_dict(mqtt_json_data_t1))
    sched1.add_schedule(convert_schedule_json_to_dict(mqtt_json_data_t2))
    print(sched1.schedules[1]['cycle'])
