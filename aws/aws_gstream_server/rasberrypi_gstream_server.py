import signal
import subprocess
import sys
import time

# Handle `Ctrl+C` gracefully with signal handler
def handle_interrupt(signal, frame):
    print("\nInterrupt received! Cleaning up GStreamer processes...")
    stop_g_stream_pipeline()
    sys.exit(0)  # Exit the program cleanly after cleanup

# Set up signal handler for keyboard interrupt (Ctrl+C)
signal.signal(signal.SIGINT, handle_interrupt)

def stop_g_stream_pipeline():
    """Gracefully stop GStreamer processes and force kill if necessary."""
    print("Attempting to stop GStreamer processes gracefully...")
    result = subprocess.run(
        ["pkill", "-TERM", "-f", "gst-launch-1.0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # To handle output as a string
    )

    if result.stderr:
        print("Error during graceful cleanup with `pkill`:\n", result.stderr)
    else:
        print("Gracefully sent SIGTERM to GStreamer processes.\n")

    # Wait a moment for the processes to clean up
    time.sleep(1)

    # Check if there are still any lingering gst-launch-1.0 processes
    result_check = subprocess.run(
        ["pgrep", "-f", "gst-launch-1.0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result_check.stdout:
        print("Still running gst-launch-1.0 processes:\n", result_check.stdout)
    else:
        print("No lingering gst-launch-1.0 processes found.")

    # If there are still processes running, forcefully kill them
    if result_check.stdout:
        print("Forcefully killing remaining gst-launch-1.0 processes...")
        result_force = subprocess.run(
            ["pkill", "-9", "-f", "gst-launch-1.0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result_force.stderr:
            print("Error during forceful cleanup with `pkill`:\n", result_force.stderr)
        else:
            print("Forcefully terminated lingering GStreamer processes.")

    # Add a delay before restarting to avoid rapid restarts
    time.sleep(1)

def start_gstreamer_pipeline(host: str, port: int):
    """Start the GStreamer pipeline to stream video."""
    gst_command = [
        "gst-launch-1.0",
        "v4l2src", "device=/dev/video0",
        "!", "video/x-raw,width=640,height=480,framerate=30/1",
        "!", "videoconvert",
        "!", "x264enc", "tune=zerolatency", "bitrate=500",
        "!", "rtph264pay", "config-interval=1", "pt=96",
        "!", "udpsink", f"host={host}", f"port={port}"
    ]

    try:
        # Launch the GStreamer pipeline
        process = subprocess.Popen(gst_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"GStreamer pipeline started, streaming to {host}:{port}")

        # Wait for process to finish (handle stdout, stderr)
        stdout, stderr = process.communicate()

        if stdout:
            print(stdout.decode())
        if stderr:
            print(stderr.decode())

        # Check process exit code
        if process.returncode != 0:
            print(f"GStreamer pipeline terminated with error code {process.returncode}")
            stop_g_stream_pipeline()

    except KeyboardInterrupt:
        # Handle the case where Ctrl+C is pressed during the main loop
        print("KeyboardInterrupt caught in main loop.")
        stop_g_stream_pipeline()
        sys.exit(0)

    except FileNotFoundError:
        # Handle the case where `gst-launch-1.0` is not found
        print("GStreamer is not installed or `gst-launch-1.0` is not in PATH.")
        stop_g_stream_pipeline()
        sys.exit(0)

    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"An error occurred: {e}")
        stop_g_stream_pipeline()
        sys.exit(1)

    finally:
        # Ensure the GStreamer process is terminated
        if process.poll() is None:
            process.terminate()
            process.wait()
            print("GStreamer pipeline terminated and cleaned up with process.terminate().")


if __name__ == "__main__":
    # Example usage
    host_ip_default = "127.0.0.1"  # If you want to host on Raspberry Pi itself

    # Server IP variable
    jetson_nano_ip = "100.71.196.8"
    raspberrypi_ip = "100.126.63.67"
    msi_ip = "100.72.146.99"
    aws_ip = "100.97.35.29"

    port_number = 5000

    try:
        start_gstreamer_pipeline(aws_ip, port_number)
    except Exception as e:
        print(f"Unexpected error: {e}")
        stop_g_stream_pipeline()
        sys.exit(1)
