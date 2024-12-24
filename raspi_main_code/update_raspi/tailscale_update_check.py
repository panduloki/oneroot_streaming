from subprocess_command import run_command

#TODO git reset --hard origin/main if any error to pull
#TODO update tailscale updates to logs
def check_tailscale_status():
    try:
        print("checking tailscale status .....")
        result = run_command(['tailscale', 'status'])
        if result.returncode == 0:
            print("Tailscale status command was working.")
            # print(f"tailscale status Output: {result.stdout}")
        else:
            print("Tailscale status command was not working.")
            #print(f"tailscale status error: {result.stderr}")
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
            print(f"Failed to start Tailscale up command ")
    except FileNotFoundError:
        print("Tailscale is not installed or not in the system PATH.")

if __name__ == "__main__":
    check_tailscale_status()