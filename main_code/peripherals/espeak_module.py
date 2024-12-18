import os
import shutil

def check_espeak_installed():
    # Check if espeak is installed
    if shutil.which("espeak") is None:
        print("Error: espeak is not installed. Please install it and try again.")
        return True
    else:
        print("espeak is not installed.")
        return False

def read_text_using_espeak(message):
    """
    Use espeak to read the given message aloud.
    Check if espeak is installed before attempting to use it.
    """
    # Speak the message using espeak
    os.system(f'espeak "{message}"')