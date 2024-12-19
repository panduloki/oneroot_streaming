import RPi.GPIO as GPIO

def is_pin_in_use(pin):
    try:
        GPIO.setup(pin, GPIO.IN)
        return False
    except RuntimeError:
        return True

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)  # or GPIO.BOARD
    pin = 17  # Replace with the pin number you want to check
    if is_pin_in_use(pin):
        print(f"GPIO pin {pin} is currently in use.")
    else:
        print(f"GPIO pin {pin} is not in use.")
    GPIO.cleanup()