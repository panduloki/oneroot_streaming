
"""To make a Raspberry Pi read out loud a text message using Python, you can use a text-to-speech (TTS) library like pyttsx3, which works offline and is compatible with Raspberry Pi. Here's a simple example of how to do it:

    Step 1: Install pyttsx3
    First, install the pyttsx3 library. You can do this by running the following command in your terminal:
        pip install pyttsx3
"""

import pyttsx3


def read_text(message):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech (default is 200)
    engine.setProperty('volume', 0.8)  # Volume level (0.0 to 1.0)

    # Speak the message
    engine.say(message)

    # Wait for the speech to finish before closing
    engine.runAndWait()


# Example usage
text_message = "Hello, this is a test message from the Raspberry Pi!"
read_text(text_message)
