try:
    import RPi.GPIO as GPIO  # Import the real GPIO library if running on Raspberry Pi
except (ImportError, RuntimeError):
    # If you're not on a Raspberry Pi, use the mock version
    from mock_gpio import GPIO

# GPIO-Modus auf BCM setzen
GPIO.setmode(GPIO.BCM)

class Device:

    def __init__(self, name, output, ground):
        self.NAME = name
        self.OUTPUT = output
        self.GROUND = ground

    def switch_state(self, state):
        if state == "ON":
            GPIO.output(self.OUTPUT, GPIO.HIGH)
            print(f"Device >{self.NAME}< turned on!")
        elif state == "OFF":
            GPIO.output(self.OUTPUT, GPIO.LOW)
            print(f"Device >{self.NAME}< turned off!")
        else:
            print("Invalid state! Use 'ON' or 'OFF'.")