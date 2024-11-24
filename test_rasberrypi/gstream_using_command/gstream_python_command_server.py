import subprocess
import time
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
        # Real-time monitoring of the process output
        #while True:
        #    output_line = process.stdout.readline()  # Read a line from stdout
        #    error_line = process.stderr.readline()  # Read a line from stderr
        #    
        #    if output_line:
        #       print(f"[GStreamer Output]: {output_line.strip()}")
        #    if error_line:
        #        print(f"[GStreamer Error]: {error_line.strip()}")
        #   
        #    # Check if the process has terminated
        #   if process.poll() is not None:
        #        break

        # Print any remaining output
        stdout, stderr = process.communicate()
        if stdout:
            print(stdout)
        if stderr:
            print(stderr)
        
    except FileNotFoundError:
        print("GStreamer is not installed or `gst-launch-1.0` is not in PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the process is terminated
        if process.poll() is None:
            process.terminate()
            process.wait()
            print("GStreamer pipeline terminated and cleaned up  with process.terminate().")
        
        # Kill any lingering GStreamer processes and capture errors
        result = subprocess.run(
            ["pkill", "-f", "gst-launch-1.0"],
            stderr=subprocess.PIPE,
            text=True  # To handle output as a string
            )
            
        if result.stderr:
            print("Error during cleanup with `pkill`:\n", result.stderr)
        else:
            print("GStreamer processes cleaned up successfully with pkill gst-launch-1.0q.\n")
        
        # Add a delay before restarting to avoid rapid restarts
        time.sleep(1)
        
if __name__ == "__main__":
    # Example usage
    host_ip_default = "127.0.0.1"   # if you want to host on rasberry pi itself
    
    # windows_ip or receivers_ip like jetson nano
    jetson_nano_ip = "100.71.196.8"
    windows_ip = "100.72.146.99"
    port_number = 5000
    start_gstreamer_pipeline(jetson_nano_ip, port_number)
