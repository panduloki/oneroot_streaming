import subprocess
import os
import sys

raspberry_pi_main_code_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
utils_dir = os.path.join(raspberry_pi_main_code_directory, 'utils')



# Add the main directory to sys.path to allow importing modules from the main folder
sys.path.append(raspberry_pi_main_code_directory)
sys.path.append(utils_dir)


from utils.json_writer import JSONHandler
from utils.raspi_logging import Logger


# Define log file
CAM_LOG_FILE_PATH = os.path.join(raspberry_pi_main_code_directory, 'logs', 'camera_check.log')
cam_logger = Logger(CAM_LOG_FILE_PATH)

# get parameters.json file path
parameters_path = os.path.join(utils_dir, 'parameters.json')
parameter_object = JSONHandler(parameters_path)

def check_usb_camera():
    """Check if a USB camera is connected to the Raspberry Pi."""
    global cam_logger, parameter_object, parameters_path
    try:
        # Run the v4l2-ctl command to list video devices
        cam_command_result = subprocess.run(['v4l2-ctl', '--list-devices'], capture_output=True, text=True)
        cam_logger.log_message(f"\n<------------- Checking camera ------------->", use_speaker=False)
        cam_logger.log_message(f"v4l2-ctl result: {cam_command_result.stdout}", use_speaker=False)
        #print(f"Checking camera using v4l2-ctl result: {cam_command_result.stdout}")

        if 'USB Camera' in cam_command_result.stdout:
            cam_logger.log_message("usb cam is connected.")
            parameter_object.update_value_to_key("camera_connected", True)
            cam_logger.log_message("Camera connected set to True in parameters.json")
            parameter_object.save_json_file(parameters_path)   
            return True
        else:
            cam_logger.log_error("usb cam is not connected.")
            parameter_object.update_value_to_key("camera_connected", False)
            cam_logger.log_message("Camera connected set to False in parameters.json")
            parameter_object.save_json_file(parameters_path)
            return False
        
                 
    except subprocess.CalledProcessError as e:
        cam_logger.log_error(f"An error occurred while checking the Camera connection: {e}, Return code: {e.returncode}")
    except OSError as e:
        cam_logger.log_error(f"An OS error occurred while checking camera check: {e}")
    return None
