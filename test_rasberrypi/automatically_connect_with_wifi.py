import subprocess

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
        print("Error to scan and list all wifi networks available using iwlist command:", e)
        return []

def get_saved_networks_from_config():
    """Read saved networks from wpa_supplicant.conf."""
    saved_ssids = []
    try:
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r') as file:
            for line in file:
                if 'ssid="' in line:
                    ssid = line.split('ssid="')[1].split('"')[0]
                    saved_ssids.append(ssid)
    except FileNotFoundError:
        print("wpa_supplicant.conf not found!")
    return saved_ssids


def get_saved_networks_using_nmcli():
    """Retrieve saved Wi-Fi networks using nmcli."""
    saved_ssids = []
    try:
        # Run nmcli command to list saved Wi-Fi connections
        result = subprocess.run(['nmcli', '-t', '-f', 'NAME,TYPE', 'connection', 'show'], 
                                capture_output=True, text=True, check=True)
        
        # Extract Wi-Fi SSIDs (filter for 'wifi' connections)
        for line in result.stdout.strip().split('\n'):
            name, conn_type = line.split(":")
            if conn_type == "802-11-wireless":  # Wi-Fi connection type
                saved_ssids.append(name)
    except subprocess.CalledProcessError as e:
        print("Error retrieving saved wifi networks using nmcli command :", e)
    return saved_ssids

def connect_to_wifi_using_nmcli(ssid):
    """Connect to a known Wi-Fi network."""
    try:
        subprocess.run(['sudo', 'nmcli', 'device', 'wifi', 'connect', ssid], check=True)
        print(f"Successfully connected to {ssid}")
    except subprocess.CalledProcessError as e:
        print("Failed to connect to wifi using command nmcli :", e)

# Main Logic
networks = scan_and_list_wifi_networks()
print("Available Networks:", networks)

known_ssids = get_saved_networks_using_nmcli()
print("Known Networks:", known_ssids)

# Attempt to connect if known
for ssid in networks:
    if ssid in known_ssids:
        print(f"Connecting to {ssid}")
        #connect_to_wifi(ssid)
        break
else:
    print("no available wifi networks are in list of saved networks.")
