import subprocess
import os
import signal
import sys

def start_camera_stream(device: str, host: str, port: int):
    """
    Starts a video stream for a given camera device and sends it over UDP.

    Args:
        device (str): The camera device path (e.g., "/dev/video0").
        host (str): The IP address of the host to send the stream to.
        port (int): The port number for the UDP stream.
    """
    gst_command = [
        "gst-launch-1.0",
        "v4l2src", f"device={device}",
        "!", "video/x-raw,width=640,height=480,framerate=30/1",
        "!", "videoconvert",
        "!", "x264enc", "tune=zerolatency", "bitrate=500",
        "!", "rtph264pay", "config-interval=1", "pt=96",
        "!", "udpsink", f"host={host}", f"port={port}"
    ]

    try:
        # Start the GStreamer pipeline
        print(f"Starting camera stream for {device} to {host}:{port}...")
        process = subprocess.Popen(gst_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        # Wait for process to complete
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"Error occurred while streaming from {device}: {stderr.decode()}")
        else:
            print(f"Camera stream for {device} started successfully.")

    except FileNotFoundError:
        print("Error: GStreamer is not installed or `gst-launch-1.0` is not available in PATH.")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

def signal_handler(sig, frame):
    """
    Handles the termination signal to gracefully stop camera streaming.
    """
    print("\nTermination signal received. Stopping camera streams...")
    # Send termination signal to all child processes (if required).
    sys.exit(0)

if __name__ == "__main__":
    jetson_nano_ip = "100.71.196.8"
    port0 = 5000
    port1 = 5001

    # Register signal handler for graceful exit
    signal.signal(signal.SIGINT, signal_handler)

    # Start dual camera streams
    try:
        # Start camera streams concurrently
        process0 = subprocess.Popen(
            ["gst-launch-1.0",
             "v4l2src", "device=/dev/video0",
             "!", "video/x-raw,width=640,height=480,framerate=30/1",
             "!", "videoconvert",
             "!", "x264enc", "tune=zerolatency", "bitrate=500",
             "!", "rtph264pay", "config-interval=1", "pt=96",
             "!", "udpsink", f"host={jetson_nano_ip}", f"port={port0}"],
            stderr=subprocess.PIPE, stdout=subprocess.PIPE
        )

        process1 = subprocess.Popen(
            ["gst-launch-1.0",
             "v4l2src", "device=/dev/video2",
             "!", "video/x-raw,width=640,height=480,framerate=30/1",
             "!", "videoconvert",
             "!", "x264enc", "tune=zerolatency", "bitrate=500",
             "!", "rtph264pay", "config-interval=1", "pt=96",
             "!", "udpsink", f"host={jetson_nano_ip}", f"port={port1}"],
            stderr=subprocess.PIPE, stdout=subprocess.PIPE
        )

        print("Dual camera streams started successfully.")
        # Wait for the processes to complete
        process0.wait()
        process1.wait()

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received. Stopping camera streams...")
        process0.terminate()
        process1.terminate()
        process0.wait()
        process1.wait()

    finally:
        print("Exiting script.")
