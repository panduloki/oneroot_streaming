import os
import subprocess
import sys
import time

raspberry_pi_main_code_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
utils = os.path.join(raspberry_pi_main_code_directory, 'utils')

# Add the main directory to sys.path to allow importing modules from the main folder
sys.path.append(raspberry_pi_main_code_directory)
sys.path.append(utils)

from utils.raspi_logging import Logger

# Setup logging
# Define log file
LOG_FILE = os.path.join(raspberry_pi_main_code_directory, 'logs', 'wifi_connection_logs.log')
logger = Logger(LOG_FILE)

def is_connected_to_wifi():
    """Check if connected to Wi-Fi and return the connected network name if true."""
    try:
        # Run the 'nmcli' command to get the connected Wi-Fi SSID
        result = subprocess.run(
            ['nmcli', '-t', '-f', 'ACTIVE,SSID', 'device', 'wifi'],
            capture_output=True,
            text=True,
            check=True
        )

        nmcli_output = result.stdout.strip()

        logger.log_message(f"Checking Wi-Fi connection nmcli result: {nmcli_output}")

        for line in nmcli_output.split('\n'):
            try:
                active, ssid = line.split(':')
                if active == 'yes':
                    logger.log_message(f"Connected to Wi-Fi network: {ssid}")
                    return ssid
            except ValueError:
                logger.log_error(f"Unexpected line format: {line}")

        logger.log_error("Raspi not connected to any Wi-Fi network.")
        return False
    except subprocess.CalledProcessError as e:
        logger.log_error(f"Error checking Wi-Fi connection: {e}")
        return False
    except Exception as e:
        logger.log_error(f"Error checking Wi-Fi connection: {str(e)}")
    return False

def connect_to_wifi_using_nmcli(ssid, password=None):
    """Connect to a known Wi-Fi network, optionally using a password.
    
        if password is not None:
        ssid (str): The SSID of the Wi-Fi network.
        password (str, optional): The password for the Wi-Fi network. Defaults to None.
    """
    try:
        if password:
            # Connect to the Wi-Fi network using SSID and password
            result = subprocess.run(['sudo', 'nmcli', 'device', 'wifi', 'connect', ssid, 'password', password], capture_output=True, text=True)
            if result.returncode != 0:
                logger.log_error(f"Failed to connect to Wi-Fi network '{ssid}': {result.stderr}")
                return
            if result.returncode != 0:
                logger.log_error(f"Failed to connect to Wi-Fi network '{ssid}': {result.stderr}")
            result = subprocess.run(['sudo', 'nmcli', 'device', 'wifi', 'connect', ssid], capture_output=True, text=True)
            if result.returncode != 0:
                logger.log_error(f"Failed to connect to Wi-Fi network '{ssid}': {result.stderr}")
                return
        else:
            # Connect to the Wi-Fi network without a password
            result = subprocess.run(['sudo', 'nmcli', 'device', 'wifi', 'connect', ssid], capture_output=True, text=True)
            if result.returncode != 0:
                logger.log_error(f"Failed to connect to Wi-Fi network '{ssid}': {result.stderr}")
                return

        logger.log_message(f"Successfully connected to Wi-Fi network: {ssid}")
    except subprocess.CalledProcessError as e:
        logger.log_error(f"Failed to connect to Wi-Fi network '{ssid}': {e}")

def scan_and_list_wifi_networks():
    """List available Wi-Fi networks.
    
    Returns:
        list: A list of available Wi-Fi network SSIDs.
    """
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'device', 'wifi', 'list'], capture_output=True, text=True, check=True)
        logger.log_message(f"Scanning Wi-Fi networks result: {result.stdout}")
        networks = set()
        for line in result.stdout.split('\n'):
            if line:
                networks.add(line.strip())
        return list(networks)
    except subprocess.CalledProcessError as e:
        logger.log_error(f"Error scanning Wi-Fi networks: {e}")
        return []

def get_saved_networks_using_nmcli():
    """Retrieve saved Wi-Fi networks using nmcli."""
    saved_ssids = []
    try:
        # Run nmcli command to list saved Wi-Fi connections
        result = subprocess.run(['nmcli', '-t', '-f', 'NAME,TYPE', 'connection', 'show'], capture_output=True, text=True, check=True)
        logger.log_message(f"Saved Wi-Fi networks result: {result.stdout}")
        # Extract Wi-Fi SSIDs (filter for 'Wi-Fi' connections)
        for line in result.stdout.strip().split('\n'):
            name, conn_type = line.split(":")
            if conn_type == "802-11-wireless":  # Wi-Fi connection type
                saved_ssids.append(name)
    except subprocess.CalledProcessError as e:
        logger.log_error(f"Error retrieving saved Wi-Fi networks: {e}")
    return saved_ssids

def scan_and_connect_to_first_open_wifi():
    """Automatically scans for open Wi-Fi networks and connects to the first available one."""
    try:
        # Scan for available Wi-Fi networks
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID,SECURITY', 'device', 'wifi', 'list'], capture_output=True, text=True, check=True)
        logger.log_message(f"Scanning for open Wi-Fi networks result: {result.stdout}")
        # Parse the output to find open networks (SECURITY = "--")
        for line in result.stdout.strip().split('\n'):
            if line:
                ssid2, security = line.split(":")
                if security.strip() == "--":  # Open network has no security
                    logger.log_message(f"Open network found: {ssid2}")
                    connect_to_wifi_using_nmcli(ssid2)
                    logger.log_message(f"Successfully connected to {ssid2}")
                    return

        logger.log_error("No open Wi-Fi networks found to connect.")
    except subprocess.CalledProcessError as e:
        logger.log_error(f"Error during scanning or connection: {e}")

def check_and_connect_raspi_wifi():
    run_wifi_scan = True
    max_retries = 5
    retries = 1
    while run_wifi_scan and retries <= max_retries:
        logger.log_message(f"({retries}/{max_retries}) Raspi checking and connecting to available Wi-Fi ...")
        wifi_connected_name = is_connected_to_wifi()
        if not wifi_connected_name:
            logger.log_message("Raspi not connected to Wi-Fi, checking saved networks.")
            # scan available networks
            networks = scan_and_list_wifi_networks()
            logger.log_message(f"Available Networks around raspi after scanning: {networks}")

            # Get saved Wi-Fi networks
            known_ssids = get_saved_networks_using_nmcli()
            logger.log_message(f"Saved Wi-Fi networks in raspi: {known_ssids}")

            # Attempt to connect to known networks

            for ssid in networks:
                if ssid in known_ssids:
                    logger.log_message(f"Connecting to saved Wi-Fi network: {ssid}")
                    logger.log_message(f"raspi connected exiting wifi connect loop")
                    connect_to_wifi_using_nmcli(ssid)
                    run_wifi_scan = False
                    break

            if run_wifi_scan:
                logger.log_message("Attempting to connect to any open networks.")
                scan_and_connect_to_first_open_wifi()
                logger.log_error("Wi-Fi connection failed, retrying in 10 seconds.")
            time.sleep(10)
        else:
            logger.log_message(f"Raspi already connected to Wi-Fi network: {wifi_connected_name}")
            run_wifi_scan = False
        
        retries += 1
        if retries >= max_retries:
            logger.log_error("Max retries reached. Exiting Wi-Fi connection attempts.")
            run_wifi_scan=False
            break
