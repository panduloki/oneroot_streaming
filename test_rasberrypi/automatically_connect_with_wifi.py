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

def connect_to_wifi_using_nmcli(ssid1):
    """Connect to a known Wi-Fi network."""
    try:
        subprocess.run(['sudo', 'nmcli', 'device', 'wifi', 'connect', ssid1], check=True)
        print(f"Successfully connected to {ssid1}")
    except subprocess.CalledProcessError as e:
        print("Failed to connect to wifi using command nmcli :", e)

def get_current_connected_wifi_using_nmcli():
    """
    Get the list of connected Wi-Fi networks using nmcli.
    """
    try:
        # Run nmcli command to check active connections
        result = subprocess.run(
            ['nmcli', '-t', '-f', 'ACTIVE,SSID', 'connection', 'show'],
            capture_output=True,
            text=True,
            check=True
        )
        connected_networks = []

        # Parse output
        for line in result.stdout.strip().split('\n'):
            fields = line.split(":")
            if len(fields) == 2 and fields[0] == "yes":  # ACTIVE == yes
                connected_networks.append(fields[1])  # SSID

        return connected_networks

    except subprocess.CalledProcessError as e:
        print("Error retrieving already connected Wi-Fi networks using nmcli command:", e)
        return []

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
            print(f"Open networks found: {open_networks_list}")
            # Attempt to connect to the first open network
            open_ssid = open_networks_list[0]
            connect_result = subprocess.run(
                ['sudo', 'nmcli', 'device', 'wifi', 'connect', open_ssid],
                capture_output=True, text=True, check=True
            )
            print(f"Successfully connected to {open_ssid}. command result:{connect_result}")
        else:
            print("No open Wi-Fi networks found to connect.")
    except subprocess.CalledProcessError as e:
        print(f"Error during scanning or connection: {e.stderr}")



# Main execution
if __name__ == "__main__":

    # scan available networks
    networks = scan_and_list_wifi_networks()
    print("Available Networks after scanning:", networks)

    # print already connected networks
    current_connected_networks = get_current_connected_wifi_using_nmcli()
    print("Already connected Wi-Fi Networks:", current_connected_networks)

    # print saved wifi networks
    known_ssids = get_saved_networks_using_nmcli()
    print("Known Networks:", known_ssids)

    # if not connected to any networks, automatically connect to open network
    #scan_and_connect_to_open_wifi_using_nmcli()


    # Attempt to connect if known
    for ssid in networks:
        if ssid in known_ssids:
            print(f"Connecting to {ssid}")
            #connect_to_wifi(ssid)
            break
    else:
        print("no available wifi networks are in list of saved networks.")
