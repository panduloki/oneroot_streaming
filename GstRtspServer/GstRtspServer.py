import subprocess
import sys
import socket
import requests
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GstRtspServer

# Initialize GStreamer
Gst.init(None)


# Function to check if the device is available
def check_device_available(device_path):
    # Function to list all available camera devices and store paths in a list
    def list_available_devices():
        """List all video devices under /dev and check their availability."""
        devices = []
        try:
            # Get a list of all video devices (usually named /dev/video*)
            result = subprocess.run(['ls', '/dev'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            device_list = result.stdout.decode().split()

            # Filter only video devices (e.g., /dev/video0, /dev/video1, etc.)
            for device in device_list:
                if device.startswith("video"):
                    path = f"/dev/{device}"
                    devices.append(path)

            # Print the list of detected video devices
            print("Available camera devices:", devices)
        except Exception as e:
            print(f"Error listing devices: {e}")
        return devices

    list_available_devices()

    """Check if the device (camera) is available by checking the /dev/video* path."""
    try:
        # List all video devices and check if the given device path exists
        result = subprocess.run(['ls', device_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking device: {e}")
        return False

# Function to check for MIPI (nvarguscamerasrc) camera
def check_mipi_camera():
    """Check if nvarguscamerasrc (MIPI camera) is available by inspecting system logs."""

    # Function to list all available camera devices and store paths in a list
    def list_available_devices():
        """List all video devices under /dev and check their availability."""
        devices = []
        try:
            # Get a list of all video devices (usually named /dev/video*)
            result = subprocess.run(['ls', '/dev'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            device_list = result.stdout.decode().split()

            # Filter only video devices (e.g., /dev/video0, /dev/video1, etc.)
            for device in device_list:
                if device.startswith("video"):
                    path = f"/dev/{device}"
                    devices.append(path)

            # Print the list of detected video devices
            print("Available camera devices:", devices)
        except Exception as e:
            print(f"Error listing devices: {e}")
        return devices
    try:
        result = subprocess.run(['dmesg', '|', 'grep', '-i', 'camera'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("MIPI camera detected")
            return True
        else:
            print("MIPI camera not detected")
            return False
    except Exception as e:
        print(f"Error checking MIPI camera: {e}")
        return False

# Function to get local IP address
def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Uses Google's DNS server to find local IP
            return s.getsockname()[0]
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return None

# Function to get global IP address
def get_global_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        if response.status_code == 200:
            return response.json()["ip"]
        else:
            print("Could not retrieve global IP. Status code:", response.status_code)
            return None
    except Exception as e:
        print(f"Error getting global IP: {e}")
        return None

# Define the RTSP Server class
class VideoRTSPServer(GstRtspServer.RTSPMediaFactory):
    def __init__(self, camera_type="nvarguscamerasrc", device="/dev/video0"):
        super(VideoRTSPServer, self).__init__()
        self.set_shared(True)
        self.camera_type = camera_type
        self.device = device

    def do_create_element(self, url):
        """Create GStreamer pipeline depending on the camera type."""
        if self.camera_type == "v4l2src":
            if check_device_available(self.device):
                pipeline = (
                    f"v4l2src device={self.device} ! video/x-raw, width=640, height=480, framerate=30/1 "
                    "! nvvidconv ! video/x-raw, format=I420 "
                    "! x264enc speed-preset=ultrafast tune=zerolatency bitrate=500 "
                    "! rtph264pay config-interval=1 name=pay0 pt=96"
                )
            else:
                raise ValueError(f"USB camera device {self.device} not found.")
        else:
            if check_mipi_camera():
                pipeline = (
                    "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=640, height=480, framerate=30/1 "
                    "! nvvidconv ! video/x-raw, format=I420 "
                    "! x264enc speed-preset=ultrafast tune=zerolatency bitrate=500 "
                    "! rtph264pay config-interval=1 name=pay0 pt=96"
                )
            else:
                raise ValueError("MIPI camera not detected. Ensure the camera is connected.")
        return Gst.parse_launch(pipeline)


# Start the RTSP server
def start_rtsp_server():
    try:
        camera_type = "v4l2src"  # Change to "nvarguscamerasrc" if using MIPI camera
        device_path = "/dev/video0"  # Adjust the device path accordingly for USB camera

        # Create the RTSP server and assign the pipeline
        server = VideoRTSPServer(camera_type=camera_type, device=device_path)
        server.set_shared(True)

        # Create an RTSP server and attach the media factory
        rtsp_server = GstRtspServer.RTSPServer()
        rtsp_server.set_service("8554")
        rtsp_server.get_mount_points().add_factory("/test", server)

        print("RTSP server running at rtsp://localhost:8554/test")
        rtsp_server.attach(None)

        # Start the GStreamer main loop
        loop = GLib.MainLoop()
        loop.run()

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    start_rtsp_server()
