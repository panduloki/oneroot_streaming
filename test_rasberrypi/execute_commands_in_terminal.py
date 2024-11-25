import subprocess  # To execute shell commands
import threading  # To handle real-time monitoring using threads

def run_command(command):
    """
    Executes a command in a subprocess and monitors its output in real-time using threads.
    """
    def monitor_stream(stream, label):
        """
        Reads a stream line-by-line and prints each line with a label (e.g., STDOUT or STDERR).
        """
        for line in iter(stream.readline, ''):  # Continuously read lines until the stream ends
            print(f"{label}: {line.strip()}")  # Print the line with a label
        stream.close()  # Close the stream when done

    # Start the subprocess with pipes for stdout and stderr
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Create a thread to monitor the stdout stream
    stdout_thread = threading.Thread(target=monitor_stream, args=(process.stdout, "STDOUT"))
    # Create another thread to monitor the stderr stream
    stderr_thread = threading.Thread(target=monitor_stream, args=(process.stderr, "STDERR"))

    # Start the threads to begin real-time monitoring
    stdout_thread.start()
    stderr_thread.start()

    # Wait for the process to finish execution
    process.wait()

    # Wait for both threads to complete their monitoring
    stdout_thread.join()
    stderr_thread.join()

    # Check the return code of the process
    if process.returncode == 0:  # A return code of 0 indicates success
        print("Command executed successfully.")  # Success message
    else:
        print(f"Command failed with return code {process.returncode}")  # Error message with return code

def run_command_continuous(command):
    """
    Runs a command and monitors its output in real-time.
    Handles continuous output with the ability to stop the process.
    """
    def monitor_stream(stream, label, stop_event):
        """
        Reads a stream line-by-line and prints it with a label until the stop_event is set.
        """
        for line in iter(stream.readline, ''):
            if stop_event.is_set():  # Check if stop_event is triggered
                break  # Exit the loop if we need to stop
            print(f"{label}: {line.strip()}")
        stream.close()  # Close the stream when done

    stop_event = threading.Event()  # Event to signal when to stop monitoring

    # Start the subprocess
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Create threads for real-time monitoring
    stdout_thread = threading.Thread(target=monitor_stream, args=(process.stdout, "STDOUT", stop_event))
    stderr_thread = threading.Thread(target=monitor_stream, args=(process.stderr, "STDERR", stop_event))

    # Start the threads
    stdout_thread.start()
    stderr_thread.start()

    try:
        print("Press Ctrl+C to stop the command.")
        process.wait()  # Wait for the process to complete (blocks until terminated)
    except KeyboardInterrupt:
        # Handle user interruption (e.g., Ctrl+C)
        print("Stopping the command...")
        stop_event.set()  # Signal threads to stop monitoring
        process.terminate()  # Gracefully terminate the process
        process.wait()  # Ensure the process has terminated

    # Ensure threads complete their execution
    stdout_thread.join()
    stderr_thread.join()

    # Check the return code
    if process.returncode == 0:
        print("Command executed successfully.")
    else:
        print(f"Command failed or was stopped with return code {process.returncode}.")

# Example usage
run_command(["ping", "-c", "4", "google.com"])  # Ping Google's server 4 times

# Example usage with a continuous command
run_command_continuous(["ping", "google.com"])  # Ping Google continuously
