import subprocess
import os
import sys

raspberry_pi_main_code_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
utils_dir = os.path.join(raspberry_pi_main_code_directory,'raspi_main_code', 'utils')
main_dir = os.path.join(raspberry_pi_main_code_directory,'raspi_main_code')


# Add the main directory to sys.path to allow importing modules from the main folder
sys.path.append(raspberry_pi_main_code_directory)
sys.path.append(utils_dir)
sys.path.append(main_dir)

from json_writer import JSONHandler
from utils.raspi_logging import Logger


# Define log file
LOG_FILE = os.path.join(main_dir, 'logs', 'camera_check.log')
logger = Logger(LOG_FILE)

# get parameters.json file path
parameters_path = os.path.join(raspberry_pi_main_code_directory, 'raspi_main_code', 'parameters.json')
parameter_object = JSONHandler(parameters_path)

def check_usb_camera():
    try:
        # Run the v4l2-ctl command to list video devices
        cam_command_result = subprocess.run(['v4l2-ctl', '--list-devices'], capture_output=True, text=True)
        logger.log_message(f"Checking microphone v4l2-ctl result: {cam_command_result.stdout}")

        if 'video' in cam_command_result.stdout:
            logger.log_message("usb cam is connected.")
            parameter_object.update("camera_connected", True)
            logger.log_message("Camera connected set to True in parameters.json")
            return True
        else:
            logger.log_error("usb cam is not connected.")
            parameter_object.update("camera_connected", False)
            logger.log_message("Camera connected set to False in parameters.json")
            return False
    except subprocess.CalledProcessError as e:
        logger.log_error(f"An error occurred while checking the Camera connection: {e}, Return code: {e.returncode}")
    except OSError as e:
        logger.log_error(f"An OS error occurred while checking camera check: {e}")
    return None
