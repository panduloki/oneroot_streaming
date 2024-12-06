import time
from gpiozero import Button, LED
from signal import pause

# Setup
button = Button(18)
led = LED(17)
toggle_state = False
press_start = None

# Short press: Toggle LED
def on_press():
    global press_start
    press_start = time.time()

def on_release():
    global press_start, toggle_state
    press_duration = time.time() - press_start

    if press_duration < 1:  # Short press (less than 1 second)
        toggle_state = not toggle_state
        if toggle_state:
            led.on()
            print("LED toggled ON")
        else:
            led.off()
            print("LED toggled OFF")
    elif press_duration >= 1:  # Long press (1 second or more)
        led.blink(on_time=0.2, off_time=0.2, n=5)
        print("LED blinking (long press action)")

# Assign callbacks
button.when_pressed = on_press
button.when_released = on_release

# Keep the script running
print("Short press toggles LED. Long press blinks LED.")
pause()
