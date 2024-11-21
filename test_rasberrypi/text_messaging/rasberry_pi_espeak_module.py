import os

#sudo apt install espeak
"""
Step 1: Verify Audio Output Device
Since your list shows multiple playback devices, ensure the Raspberry Pi is set to the correct output (e.g., HDMI or Headphones).

Check Current Output Device: Run the following command:


amixer cget numid=3
This will show the current output device:

0 = Auto
1 = Headphones (3.5mm jack)
2 = HDMI
Force Audio Output: To explicitly set the output device:

bash
Copy code
amixer cset numid=3 <value>
Replace <value> with:

1 for Headphones
2 for HDMI
Step 2: Test Audio Output
Test if audio output works with a basic command:

bash
Copy code
aplay /usr/share/sounds/alsa/Front_Center.wav


"""

def read_text(message):
    # Use espeak to directly speak the message
    os.system(f'espeak "{message}"')

# Example usage
#read_text("Hello, this is a test message from your Raspberry Pi!")
