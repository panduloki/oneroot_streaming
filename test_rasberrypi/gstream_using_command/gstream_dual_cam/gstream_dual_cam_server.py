import subprocess
import threading
import time


def start_gstreamer_pipeline(device: str, host: str, port: int):
    """
    Start a GStreamer pipeline for a specific camera device.
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
        # Launch the GStreamer pipeline
        process = subprocess.Popen(gst_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"GStreamer pipeline started for {device}, streaming to {host}:{port}")

        # Keep the process running and print any errors
        while process.poll() is None:
            time.sleep(1)

    except FileNotFoundError:
        print("GStreamer is not installed or `gst-launch-1.0` is not in PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the process is terminated
        if process.poll() is None:
            process.terminate()
            process.wait()
            print(f"GStreamer pipeline for {device} terminated.")

        # Cleanup lingering processes for the specific device
        subprocess.run(["pkill", "-f", f"v4l2src device={device}"], stderr=subprocess.PIPE, text=True)


def run_dual_camera_streaming():
    devices = ["/dev/video0", "/dev/video1"]
    host_ip = "100.71.196.8"  # Replace with Jetson Nano or desired receiver's IP
    ports = [5000, 5001]

    threads = []
    for device, port in zip(devices, ports):
        thread = threading.Thread(target=start_gstreamer_pipeline, args=(device, host_ip, port))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete (optional)
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    run_dual_camera_streaming()
