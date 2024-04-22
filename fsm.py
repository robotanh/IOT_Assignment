from datetime import datetime
from rs485 import *
from timer import *
import json

PHYSIC = False


class FarmScheduler():
    def __init__(self, debug=False):
        self.debug = debug
        self.schedules = []
        self.current_schedule = None
        self.current_state = IdleState(debug=self.debug)

    def run(self):
        if not self.current_schedule:
            self.current_schedule = self.check_schedule()
            if not self.current_schedule:
                return

        self.current_state.execute(self.current_schedule)

    def add_schedule(self, schedule):
        self.schedules.append(schedule)

    def check_schedule(self):
        now = datetime.now().strftime("%H:%M")
        for schedule in self.schedules:
            if now == schedule['startTime']:
                return schedule
        return None


class State:
    def __init__(self, debug=False):
        self.debug = debug

    def execute(self, schedule):
        raise NotImplementedError


class IdleState(State):
    def execute(self, schedule):
        if self.debug:
            print("IDLE STATE")
        if schedule['cycle'] > 0:
            self.next_state = Mixer1State(debug=self.debug)
            self.next_state.execute(schedule)
            schedule['cycle'] -= 1
        else:
            print("FINISHED !!!")


class Mixer1State(State):
    def execute(self, schedule):
        if self.debug:
            print("MIXER1 STATE")
        setTimer(0, int(schedule['mixer1']))
        self.next_state = Mixer2State(debug=self.debug)
        # TURN ON MIXER1
        # if PHYSIC:
        #     physic_controller.setActuators(MIXER1, True)
        # # Assume timer_flag is managed somewhere else


class Mixer2State(State):
    def execute(self, schedule):
        if self.debug:
            print("MIXER2 STATE")
        setTimer(0, int(schedule['mixer2']))
        self.next_state = Mixer3State(debug=self.debug)
        # TURN OFF MIXER1 AND TURN ON MIXER2
        # if PHYSIC:
        #     physic_controller.setActuators(MIXER1, False)
        #     physic_controller.setActuators(MIXER2, True)


class Mixer3State(State):
    def execute(self, schedule):
        if self.debug:
            print("MIXER3 STATE")
        setTimer(0, int(schedule['mixer3']))
        self.next_state = PumpInState(debug=self.debug)
        # TURN OFF MIXER2 AND TURN ON MIXER3
        # if PHYSIC:
        #     physic_controller.setActuators(MIXER2, False)
        #     physic_controller.setActuators(MIXER3, True)


class PumpInState(State):
    def execute(self, schedule):
        if self.debug:
            print("PUMPIN STATE")
        setTimer(0, int(schedule['pump_in']))
        self.next_state = PumpOutState(debug=self.debug)
        # TURN OFF MIXER3 AND TURN ON PUMPIN
        # if PHYSIC:
        #     physic_controller.setActuators(MIXER3, False)
        #     physic_controller.setActuators(PUMPIN, True)


class PumpOutState(State):
    def execute(self, schedule):
        if self.debug:
            print("PUMPOUT STATE")
        setTimer(0, int(schedule['pump_out']))
        self.next_state = IdleState(debug=self.debug)
        # TURN OFF PUMPIN AND TURN ON PUMPOUT
        # if PHYSIC:
        #     physic_controller.setActuators(PUMPIN, False)
        #     physic_controller.setActuators(PUMPOUT, True)


def convert_schedule_json_to_dict(json_data):
    return json.loads(json_data)


if __name__ == '__main__':
    sched1 = FarmScheduler()
    mqtt_json_data_t1 = '{"mixer1": 3, "mixer2": 3, "mixer3": 3, "pump_in": 3, "pump_out": 3, "selector": "A", "cycle": 2, "startTime": "16:43"}'
    mqtt_json_data_t2 = '{"mixer1": 3, "mixer2": 3, "mixer3": 3, "pump_in": 3, "pump_out": 3, "selector": "A", "cycle": 2, "startTime": "15:30"}'

    sched1.add_schedule(convert_schedule_json_to_dict(mqtt_json_data_t1))
    sched1.add_schedule(convert_schedule_json_to_dict(mqtt_json_data_t2))
    print(sched1.schedules[1]['cycle'])
