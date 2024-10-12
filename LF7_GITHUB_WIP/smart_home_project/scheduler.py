import schedule
import time
from device import *

# Define devices
heater = Device('Heater', 19, 20)
coffeeMachine = Device('Coffee machine', 26, 25)
lights = Device('Lights', 29, 30)
blinds = Device('Blinds', 33, 34)
tv = Device('TV', 40, 39)

#To-Do @LUCAS
def add_routine(routine, routine_action):
    device_name = routine_action['device']
    chosenDevice = ""
    
    if device_name == "heating":
        chosenDevice = heater   
    elif device_name == "coffee maker":
        chosenDevice = coffeeMachine 
    elif device_name == "lights":
        chosenDevice = lights 
    elif device_name == "blinds":
        chosenDevice = blinds 
    elif device_name == "tv":
        chosenDevice = tv  

    job = schedule.every().day.at(routine['time'] - routine_action['offset']).do(lambda: chosenDevice.switch_state(routine_action['state'])).tag(routine['name'])
    print(f'Added {job.toString()} to scheduler!')

#To-Do @LUCAS
def remove_routine(routine):
    schedule.clear(routine['name'])
    print(f'Removed the routine {routine['name']} from scheduler!')