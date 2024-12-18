import os
import subprocess
import logging
import sys
import time

# Get the directory of the main folder (raspi_main_code)
main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the main folder to sys.path so Python can find the modules
sys.path.append(main_dir)

from raspi_main_code.json_writer import JSONHandler
from raspi_main_code.peripherals.espeak_module import read_text_using_espeak

# Setup logging
LOG_FILE = "wifi_connection_logs.txt"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# Build the path to parameters.json relative to the script directory
parameters_path = os.path.join(main_dir, "raspi_main_code", "parameters.json")

parameter_object = JSONHandler(parameters_path)

def log_message(message):
    """Log a message to the log file and print to the console."""
    logging.info(message)
    print(message)

    use_speaker = parameter_object.get("use_speaker")
    if (use_speaker is not None and use_speaker != "null") or (use_speaker == "true"):
        read_text_using_espeak(message)
    else:
        print("Speaker was not checked for connection, not using speaker by default.")

def is_connected_to_wifi():
    """Check if connected to Wi-Fi and return the connected network name if true."""
    try:
        # Run the 'nmcli' command to get the connected Wi-Fi SSID
        result = subprocess.run(
            ['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'],
            capture_output=True,
            text=True
        )

        # If the result starts with "yes", it means we are connected to a Wi-Fi network
        if result.stdout.strip().startswith("yes"):
            ssid = result.stdout.strip().split(":")[1]
            log_message(f"Connected to Wi-Fi network: {ssid} already")
            return ssid
        else:
            print("Raspi not connected to any Wi-Fi network.")
            return False
    except subprocess.CalledProcessError as e:
        log_message(f"Error checking Wi-Fi connected: {e}")
        return False
    except Exception as e:
        log_message(f"Error checking Wi-Fi connection: {str(e)}")
        return False

def connect_to_wifi_using_nmcli(ssid, password=None):
    """Connect to a known Wi-Fi network, optionally using a password."""
    try:
        if password:
            # Connect to the Wi-Fi network using SSID and password
            subprocess.run(['sudo', 'nmcli', 'device', 'wifi', 'connect', ssid, 'password', password], check=True)
        else:
            # Connect to the Wi-Fi network without a password
            subprocess.run(['sudo', 'nmcli', 'device', 'wifi', 'connect', ssid], check=True)

        log_message(f"Successfully connected to Wi-Fi network: {ssid}")
    except subprocess.CalledProcessError as e:
        log_message(f"Failed to connect to Wi-Fi network '{ssid}': {e}")

def scan_and_list_wifi_networks():
    """List available Wi-Fi networks."""
    try:
        result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True, check=True)
        networks = set()
        for line in result.stdout.split('\n'):
            if 'ESSID:' in line:
                essid = line.split(':')[1].strip().strip('"')
                networks.add(essid)
        return list(networks)
    except subprocess.CalledProcessError as e:
        log_message(f"Error to scan and list all wifi networks available using iwlist command:", e)
        return []

def get_saved_networks_using_nmcli():
    """Retrieve saved Wi-Fi networks using nmcli."""
    saved_ssids = []
    try:
        # Run nmcli command to list saved Wi-Fi connections
        result = subprocess.run(['nmcli', '-t', '-f', 'NAME,TYPE', 'connection', 'show'],
                                capture_output=True, text=True, check=True)

        # Extract Wi-Fi SSIDs (filter for 'Wi-Fi' connections)
        for line in result.stdout.strip().split('\n'):
            name, conn_type = line.split(":")
            if conn_type == "802-11-wireless":  # Wi-Fi connection type
                saved_ssids.append(name)
    except subprocess.CalledProcessError as subprocess_error:
        log_message("Error retrieving saved wifi networks using nmcli command :", subprocess_error)
    return saved_ssids

def scan_and_connect_to_open_wifi_using_nmcli():
    """
    Automatically scans for open Wi-Fi networks and connects to the first available one.
    """
    try:
        # Scan for available Wi-Fi networks
        result = subprocess.run(
            ['nmcli', '-t', '-f', 'SSID,SECURITY', 'device', 'wifi', 'list'],
            capture_output=True, text=True, check=True
        )

        # Parse the output to find open networks (SECURITY = "--")
        open_networks_list = []
        for line in result.stdout.strip().split('\n'):
            if line:
                ssid2, security = line.split(":")
                if security.strip() == "--":  # Open network has no security
                    open_networks_list.append(ssid2)

        if open_networks_list:
            log_message(f"Open networks found: {open_networks_list}")
            # Attempt to connect to the first open network
            open_ssid = open_networks_list[0]
            connect_result = subprocess.run(
                ['sudo', 'nmcli', 'device', 'wifi', 'connect', open_ssid],
                capture_output=True, text=True, check=True
            )
            log_message(f"Successfully connected to {open_ssid}. command result:{connect_result}")
        else:
            log_message("No open Wi-Fi networks found to connect.")
    except subprocess.CalledProcessError as e:
        log_message(f"Error during scanning or connection: {e.stderr}")


def checking_raspi_wifi():
    run_wifi_scan = True
    while run_wifi_scan:
        log_message("raspi checking and connecting to available wifi ...")
        wifi_connected_name = is_connected_to_wifi()
        if not  wifi_connected_name:
            log_message("since raspi not connected to wifi checking to connect with saved networks in config file")

            # scan available networks
            networks = scan_and_list_wifi_networks()
            print("Available Networks after scanning:", networks)

            # print saved wifi networks
            known_ssids = get_saved_networks_using_nmcli()
            print("Known Networks:", known_ssids)

            # Attempt to connect if known
            for ssid in networks:
                if ssid in known_ssids:
                    log_message(f"wifi name {ssid} was saved already, connecting to it")
                    connect_to_wifi_using_nmcli(ssid)
                    run_wifi_scan = False
                    break
            else:
                log_message("Error no available wifi networks are in list of saved networks.")

            log_message("Lets try to connect to any open networks")
            scan_and_connect_to_open_wifi_using_nmcli()
            if not is_connected_to_wifi():
                log_message("wifi not worked after all this steps checking after 10 seconds")
                time.sleep(10)
        else:
            log_message(f"raspi already connected to wifi name: {wifi_connected_name}")
            run_wifi_scan = False
            break




