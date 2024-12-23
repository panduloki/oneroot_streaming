from subprocess_command import run_command

def check_tailscale_status():
    try:
        print("checking tailscale status .....")
        result = run_command(['tailscale', 'status'])
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
        result = run_command(['tailscale', 'up', '--advertise-exit-node'])
        if result.returncode == 0:
            print("Tailscale up command started successfully.")
        else:
            print(f"Failed to start Tailscale up command : {result.stderr}")
    except FileNotFoundError:
        print("Tailscale is not installed or not in the system PATH.")

if __name__ == "__main__":
    check_tailscale_status()