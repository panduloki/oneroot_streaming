from gpiozero import LED
from time import sleep
import subprocess

# Set up the LED on GPIO pin 17
wifi_led = LED(17)

# Function to check Wi-Fi connection
def is_wifi_connected():
    try:
        # Use nmcli to get the connection status
        result = subprocess.run(["nmcli", "-t", "-f", "ACTIVE,SSID", "dev", "wifi"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "yes" in line:
                return True
        return False
    except Exception as e:
        print("there was an error while checking is_wifi_connected in wifi led status", e)
        return False

# Blink pattern: slow for connected, fast for disconnected
def blink_led():
    while True:
        if is_wifi_connected():
            # Slow blink (Wi-Fi connected)
            wifi_led.on()
            sleep(1)
            wifi_led.off()
            sleep(1)
        else:
            # Fast blink (Wi-Fi disconnected)
            wifi_led.on()
            sleep(0.2)
            wifi_led.off()
            sleep(0.2)

# Run the blink pattern
print("Starting Wi-Fi LED indicator...")
blink_led()
