import subprocess

def check_tailscale_status():
    try:
        print("checking tailscale status .....")
        result = subprocess.run(['tailscale', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Tailscale is running.")
            print(f"tailscale status Output: {result.stdout}")
        else:
            print("Tailscale is not running")
            print(f"tailscale status error: {result.stderr}")
            start_tailscale()
    except FileNotFoundError:
        print("Tailscale is not installed or not in the system PATH.")

def start_tailscale():
    try:
        print("Starting Tailscale up command ....")
        result = subprocess.run(['tailscale', 'up', '--advertise-exit-node'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Tailscale started successfully.")
        else:
            print(f"Failed to start Tailscale: {result.stderr}")
    except FileNotFoundError:
        print("Tailscale is not installed or not in the system PATH.")

if __name__ == "__main__":
    check_tailscale_status()