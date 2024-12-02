import signal
import subprocess
import sys
import time
import cv2


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


def start_gstreamer_receiver(host: str, port: int):
    # GStreamer pipeline for receiving video stream via UDP
    gst_pipeline = f"udpsrc port={port} ! application/x-rtp,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! appsink"

    # Create VideoCapture object with GStreamer pipeline
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Failed to open GStreamer pipeline.")
        return

    print(f"Receiver pipeline started on {host}:{port}")

    try:
        while True:
            # Read frame from the GStreamer pipeline
            ret, frame = cap.read()
            if ret:
                # Display the frame using OpenCV
                # cv2.imshow("Received Video Stream", frame)
                if frame is not None and frame.size > 0:
                    print("frame received size: ", frame.shape)
            else:
                print("Failed to retrieve frame from stream.")
                break

            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Receiver pipeline stopped.")
        cap.release()
        cv2.destroyAllWindows()
        stop_g_stream_pipeline()


# Example usage
if __name__ == "__main__":
    receiver_host = "0.0.0.0"  # Listen on all interfaces
    receiver_port = 5000  # The port number must match the sender
    start_gstreamer_receiver(receiver_host, receiver_port)
