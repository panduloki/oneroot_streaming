import logging
import os
import sys

from raspi_main_code.json_writer import JSONHandler
from raspi_main_code.peripherals import read_text_using_espeak


# Get the directory of the main folder (raspi_main_code) to ensure that all modules can be found
main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the main folder to sys.path so Python can find the modules
# This is necessary to ensure that the modules in the main directory
# can be imported and used in this script.
sys.path.append(main_dir)


# Build the path to parameters.json relative to the script directory
parameters_path = os.path.join(main_dir, "raspi_main_code", "parameters.json")
parameter_object = JSONHandler(parameters_path)
use_speaker = parameter_object.get("speaker_connected")

class Logger:
    """
    A Logger class to handle logging messages to a file and optionally using a speaker.
    Attributes:
        log_file_path (str): The path to the log file.
    Methods:
        __init__(log_file_path):
            Initializes the Logger with the specified log file path and configures logging.
        _configure_logging():
            Configures the logging settings such as filename, logging level, format, and date format.
        log_message(message):
            Logs a message to the log file, prints it to the console, and optionally uses a speaker to read the message.
        log_error(message):
            Logs an error message to the log file and prints it to the console.
    """
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self._configure_logging()

    def _configure_logging(self):
        """Configure the logging settings."""
        try:
            logging.basicConfig(
                filename=self.log_file_path,
                level=logging.INFO,
                format="%(asctime)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        except Exception as e:
            print(f"Failed to configure logging: {e}")
    
    def log_message(self, message):
        """Log a message to the log file and print to the console."""
        try:
            logging.info(message)
            if logging.getLogger().handlers:
                logging.getLogger().handlers[0].flush()  # Ensure logs are written to the file
            print(message)

            if use_speaker.lower() == "true":
                read_text_using_espeak(message)
            else:
                print("Speaker is not available, not using speaker by default.")
        except Exception as e:
            print(f"Failed to log message: {e}")
        
    def log_error(self, message):
        """Log an error message to the log file and print to the console in red."""
        try:
            logging.error(message)
            if logging.getLogger().handlers:
                logging.getLogger().handlers[0].flush()  # Ensure logs are written to the file
            print(f"\033[91mERROR: {message}\033[0m")  # Print error message in red

             # Check if the speaker is connected and the parameter is set to use it
            if use_speaker.lower() == "true":
                read_text_using_espeak(message)
            else:
                print("Speaker is not available, not using speaker by default.")
        except Exception as e:
            print(f"Failed to log error message: {e}")