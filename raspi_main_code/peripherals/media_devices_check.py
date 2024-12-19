import os
import subprocess
import sys


raspberry_pi_main_code_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
utils_dir = os.path.join(raspberry_pi_main_code_directory,'raspi_main_code', 'utils')
main_dir = os.path.join(raspberry_pi_main_code_directory,'raspi_main_code')


# Add the main directory to sys.path to allow importing modules from the main folder
sys.path.append(raspberry_pi_main_code_directory)
sys.path.append(utils_dir)
sys.path.append(main_dir)

from json_writer import JSONHandler
from raspi_logging import Logger


# Define log file
LOG_FILE = os.path.join(main_dir, 'logs', 'speaker_and_mic_check.log')
logger = Logger(LOG_FILE)

# get parameters.json file path
parameters_path = os.path.join(raspberry_pi_main_code_directory, 'raspi_main_code', 'parameters.json')
parameter_object = JSONHandler(parameters_path)

def check_speaker():
    try:
        with subprocess.Popen(['aplay', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
            aplay_result, _ = proc.communicate()
        logger.log_message(f"Checking speaker aplay result: {aplay_result}")
        if 'card' in aplay_result:
            logger.log_message("Speaker is connected.") 
            parameter_object.update("speaker_connected", True)
            parameter_object.save(parameters_path)
            logger.log_message("Speaker connected set to True in parameters.json")
            return True
        else:
            logger.log_error("Speaker is not connected.")
            parameter_object.update("speaker_connected", False)
            parameter_object.save(parameters_path)
            logger.log_message("Speaker connected set to False in parameters.json")
            return False
    except subprocess.CalledProcessError as e:
        logger.log_error(f"An error occurred while checking the speaker: {e}, Return code: {e.returncode}")
    except OSError as e:
        logger.log_error(f"An OS error occurred: {e}")
    return None


def check_microphone():
    try:
        arecord_result = subprocess.check_output(['arecord', '-l'], text=True, stderr=subprocess.STDOUT)
        logger.log_message(f"Checking microphone arecord result: {arecord_result}")
        if 'card' in arecord_result:
            logger.log_message("Microphone is connected.")
            parameter_object.update("microphone_connected", True)
            logger.log_message("Microphone connected set to True in parameters.json")
            return True
        else:
            logger.log_error("Microphone is not connected.")
            parameter_object.update("microphone_connected", False)
            logger.log_message("Microphone connected set to False in parameters.json")
            return False
    except subprocess.CalledProcessError as e:
        logger.log_error(f"An error occurred while checking the microphone: {e}, Return code: {e.returncode}")
    except OSError as e:
        logger.log_error(f"An OS error occurred: {e}")
    return None