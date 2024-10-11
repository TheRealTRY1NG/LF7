import schedule
import time
#import RPi.GPIO as GPIO
try:
    import RPi.GPIO as GPIO  # Import the real GPIO library if running on Raspberry Pi
except (ImportError, RuntimeError):
    # If you're not on a Raspberry Pi, use the mock version
    from mock_gpio import GPIO

LED_PIN = 18

def turn_on_led():
    GPIO.output(LED_PIN, GPIO.HIGH)
    print("Lights on!")

def turn_off_led():
    GPIO.output(LED_PIN, GPIO.LOW)
    print("Lights off!")

def add_routine(routine):
    action = routine['action']
    if action == 'turn_on':
        schedule.every().day.at(routine['time']).do(turn_on_led)
    elif action == 'turn_off':
        schedule.every().day.at(routine['time']).do(turn_off_led)

def remove_routine(routine):
    # This is a simplified method to remove jobs based on the time
    schedule.clear(routine['time'])

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
