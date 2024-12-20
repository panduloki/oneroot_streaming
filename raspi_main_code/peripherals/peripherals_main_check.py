import os
import sys

# Add the main directory to sys.path to allow importing modules from the main folder
raspberry_pi_main_code_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(raspberry_pi_main_code_directory)

main_code_directory = os.path.join(raspberry_pi_main_code_directory,'raspi_main_code')
sys.path.append(main_code_directory)

# Ensure the peripherals module is in the sys.path
peripheral_dir = os.path.join(main_code_directory, 'peripherals')
sys.path.append(peripheral_dir)

# Ensure the utils module is in the sys.path
utils_dir = os.path.join(raspberry_pi_main_code_directory,'raspi_main_code', 'utils')
sys.path.append(utils_dir)

from peripherals import media_devices_check, camera_check
from audio_play import play_audio_file_pydub

if __name__ == '__main__':
    media_devices_check.check_speaker()
    #media_devices_check.check_microphone()

    #play_audio_file_pydub('utils/audio_files/arcade_alert.wav')

    #camera_check.check_usb_camera()
