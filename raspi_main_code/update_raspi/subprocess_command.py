import subprocess

def run_command(command):
    try:
        print(f"\n<------------------ Running command: {' '.join(command)} ---------------------->")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"command:{command} Output: {result.stdout}")
        if result.stderr:
            print(f"command:{command} Error: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running command {' '.join(command)}: {e}")
        print(f"command: {command} Output: {e.output}")
        print(f"Error: {e.stderr} for command: {command}")
        return e