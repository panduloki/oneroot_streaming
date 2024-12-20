import subprocess

def run_command(command):
    try:
        print(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"command:{command} Output: {result.stdout}")
        print(f"command:{command} Error: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running command {' '.join(command)}: {e}")
        print(f"Output: {e.output}")
        print(f"Error: {e.stderr}")

def run_system_update():
    commands = [
        ['sudo', 'apt-get', 'update'],
        ['sudo', 'apt-get', 'upgrade', '-y'],
        ['sudo', 'apt-get', 'dist-upgrade', '-y'],
        ['sudo', 'apt-get', 'autoremove', '-y'],
        ['sudo', 'apt-get', 'clean']
    ]
    
    for command in commands:
        run_command(command)
    
    print("System update and cleanup completed successfully.")

