class GPIO:
    BCM = "BCM"
    OUT = "OUT"
    HIGH = True
    LOW = False

    @staticmethod
    def setmode(mode):
        print(f"Mock GPIO set mode: {mode}")

    @staticmethod
    def setup(pin, mode):
        print(f"Mock GPIO setup pin {pin} as {mode}")

    @staticmethod
    def output(pin, state):
        print(f"Mock GPIO output to pin {pin}: {'HIGH' if state else 'LOW'}")

    @staticmethod
    def cleanup():
        print("Mock GPIO cleanup")

    @staticmethod
    def setwarnings(flag):
        print(f"Mock GPIO set warnings: {flag}")
