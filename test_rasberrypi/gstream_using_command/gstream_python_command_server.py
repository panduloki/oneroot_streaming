import subprocess

def start_gstreamer_pipeline(host: str, port: int):
    # Define the GStreamer pipeline command
    # gst_command = [
    #     "gst-launch-1.0",
    #     "v4l2src", "device=/dev/video0",
    #     "!", "video/x-raw,width=640,height=480,framerate=30/1",
    #     "!", "videoconvert",
    #     "!", "video/x-raw,format=I420",
    #     "!", "x264enc",
    #     "!", "rtph264pay",
    #     "!", f"udpsink", f"host={host}", f"port={port}"
    # ]

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
        # Wait for the process to complete
        stdout, stderr = process.communicate()
        print(stdout.decode())
        print(stderr.decode())
    except FileNotFoundError:
        print("GStreamer is not installed or `gst-launch-1.0` is not in PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
host_ip_default = "127.0.0.1" # windows_ip or receivers_ip like jetson nano
jetson_nano_ip = "100.71.196.8"
windows_ip = "100.72.146.99"
port_number = 5000
start_gstreamer_pipeline(jetson_nano_ip, port_number)
