import os
import sys


raspberry_pi_main_code_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the main directory to sys.path to allow importing modules from the main folder
sys.path.append(raspberry_pi_main_code_directory)

# Ensure the utils module is in the sys.path
peripheral_dir = os.path.join(raspberry_pi_main_code_directory, 'peripherals')
sys.path.append(peripheral_dir)

from peripherals import media_devices_check

if __name__ == '__main__':
    media_devices_check.check_speaker()
    media_devices_check.check_microphone()