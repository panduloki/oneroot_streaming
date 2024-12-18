import cv2
import socket
import requests


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


# # Set up the GStreamer pipeline for RTSP streaming
# gst_pipeline = (
#     "nvarguscamerasrc ! "
#     "video/x-raw(memory:NVMM), width=640, height=480, format=(string)NV12, framerate=30/1 ! "
#     "nvvidconv ! video/x-raw, format=(string)BGRx ! "
#     "videoconvert ! video/x-raw, format=(string)BGR ! "
#     "appsink"
# )

def start_rtsp_server(destination_ip=None, port=5000):
    # Configure the GStreamer pipeline for RTSP streaming
    gst_pipeline = (
        f"v4l2src device=/dev/video0 ! "   # Capture video from USB camera
        "video/x-raw, width=640, height=480, framerate=30/1 ! "   # Resolution and frame rate
        "videoconvert ! "
        "x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! "
        "rtph264pay config-interval=1 pt=96 ! "
        f"udpsink host={destination_ip} port={port}"  # Set destination IP and port
    )

    # Start the capture using OpenCV with the GStreamer pipeline
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print("Failed to open camera with GStreamer pipeline.")
        return

    print(f"Streaming video to {destination_ip}:{port}...")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break
        # Display the frame (optional)
        cv2.imshow("RTSP Server - Jetson Nano", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Set the destination IP and port for the receiving device
    destination_ip1 = "192.168.10.65"  # Replace it with actual client IP

    port1 = 5000
    start_rtsp_server(destination_ip1, port1)
