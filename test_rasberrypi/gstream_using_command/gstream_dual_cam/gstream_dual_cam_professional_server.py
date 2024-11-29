import subprocess
import threading
import time
import os
import signal
import logging
import ipaddress

# Configure logging to provide time-stamped logs for debugging and status updates
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# A global list to keep track of active threads
threads = []


def validate_ip(ip):
    """
    Validate an IP address. Raises ValueError if the IP is invalid.
    """
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise ValueError(f"Invalid IP address: {ip}")


def validate_port(port):
    """
    Validate a port number. Raises ValueError if the port is outside the valid range (0-65535).
    """
    if not (0 <= port <= 65535):
        raise ValueError(f"Invalid port number: {port}")


def check_device_exists(device):
    """
    Check if a device exists at the specified path. Raises FileNotFoundError if the device is unavailable.
    """
    if not os.path.exists(device):
        raise FileNotFoundError(f"Device {device} does not exist or is not accessible.")


def start_gstreamer_pipeline(device, host, port):
    """
    Start a GStreamer pipeline for a specific camera device.
    Args:
        device (str): Path to the video device (e.g., /dev/video0).
        host (str): IP address to stream the video to.
        port (int): Port number for streaming.
    """
    # Validate the device path, IP address, and port before proceeding
    check_device_exists(device)
    validate_ip(host)
    validate_port(port)

    # Define the GStreamer pipeline command
    gst_command = [
        "gst-launch-1.0",
        "v4l2src", f"device={device}",  # Source: Video4Linux device
        "!", "video/x-raw,width=640,height=480,framerate=30/1",  # Video format specification
        "!", "videoconvert",  # Convert raw video to a compatible format
        "!", "x264enc", "tune=zerolatency", "bitrate=500",  # Encode the video using H.264 codec
        "!", "rtph264pay", "config-interval=1", "pt=96",  # Packetize the H.264 stream for RTP
        "!", "udpsink", f"host={host}", f"port={port}"  # Send the stream over UDP to the specified host and port
    ]

    try:
        # Start the GStreamer pipeline as a subprocess
        process = subprocess.Popen(gst_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"GStreamer pipeline started for {device}, streaming to {host}:{port}")

        # Keep the process running while it is active
        while process.poll() is None:
            time.sleep(1)
    except FileNotFoundError:
        # Handle the case where GStreamer is not installed or not in PATH
        logger.error("GStreamer is not installed or `gst-launch-1.0` is not in PATH.")
    except Exception as e:
        # Log any other exceptions
        logger.error(f"An error occurred in start_gstreamer_pipeline(): {e}")
    finally:
        # Ensure the process is terminated properly when finished
        if process.poll() is None:
            process.terminate()
            process.wait()
            logger.info(f"GStreamer pipeline for {device} terminated.")
        # Attempt to clean up lingering processes
        subprocess.run(["pkill", "-f", f"v4l2src device={device}"], stderr=subprocess.PIPE, text=True)


def signal_handler(signal, frame):
    """
    Handle termination signals (e.g., Ctrl+C) to ensure a clean shutdown.
    """
    try:
        logger.info("Termination signal received. Cleaning up...")
        for thread in threads:
            thread.join(timeout=1)  # Wait for threads to terminate gracefully
        logger.info("All threads terminated.")
        exit(0)
    except Exception as e:
        # Log any other exceptions
        logger.error(f"An error occurred in signal_handler(): {e}")


def run_dual_camera_streaming(host_ip = None, devices=None, ports=None):
    """
    Launch GStreamer pipelines for two cameras and manage them using threads.
    """

    try:
        # Create and start a thread for each camera
        if ports is None:
            print("ports should not be empty")
        elif devices is None:
            print("devices should not be empty")
        else:
            for device, port in zip(devices, ports):
                thread = threading.Thread(target=start_gstreamer_pipeline, args=(device, host_ip, port))
                thread.start()  # Start the thread
                threads.append(thread)  # Add the thread to the global list

            # Wait for all threads to finish
            for thread in threads:
                thread.join()
    except Exception as e:
        # Log any other exceptions
        logger.error(f"An error occurred in run_dual_camera_streaming(): {e}")


if __name__ == "__main__":
    # Register signal handlers for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Handle termination signals

    # Specify device paths, host IP, and port numbers
    input_devices = ["/dev/video0", "/dev/video2"]  # Paths to camera devices
    jetson_nano_ip = "100.71.196.8"  # Target IP address for streaming
    ports1 = [5000, 5001]  # Corresponding ports for each camera stream

    # Start the dual-camera streaming setup
    run_dual_camera_streaming(host_ip = jetson_nano_ip, devices=input_devices, ports=ports1)
