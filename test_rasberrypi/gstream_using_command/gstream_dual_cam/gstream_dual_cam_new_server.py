
import subprocess


def start_dual_camera_stream(host: str, port0: int, port1: int):
    """
    Starts a dual-camera stream using GStreamer.

    This function creates two video streams:
    - `/dev/video0` streams to `host:port0`.
    - `/dev/video2` streams to `host:port1`.

    The streams are encoded using H.264 with low latency and sent over UDP.

    Args:
        host (str): The IP address of the host to send the streams to.
        port0 (int): The port for the first camera stream (/dev/video0).
        port1 (int): The port for the second camera stream (/dev/video2).

    Raises:
        FileNotFoundError: If GStreamer (`gst-launch-1.0`) is not installed or found.
        subprocess.CalledProcessError: If the GStreamer pipeline fails.
        Exception: For any other unexpected errors.
    """
    # Construct the GStreamer command for dual-camera streaming

    # gst-launch-1.0 \
    # v4l2src device=/dev/video0 ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! x264enc tune=zerolatency bitrate=500 ! rtph264pay config-interval=1 pt=96 ! udpsink host=100.71.196.8 port=5000 \
    # v4l2src device=/dev/video2 ! video/x-raw,width=640,height=480,framerate=30/1 ! videoconvert ! x264enc tune=zerolatency bitrate=500 ! rtph264pay config-interval=1 pt=96 ! udpsink host=100.71.196.8 port=5001

    gst_command = [
        "gst-launch-1.0",
        "v4l2src", "device=/dev/video0",
        "!", "video/x-raw,width=640,height=480,framerate=30/1",
        "!", "videoconvert",
        "!", "x264enc", "tune=zerolatency", "bitrate=500",
        "!", "rtph264pay", "config-interval=1", "pt=96",
        "!", "udpsink", f"host={host}", f"port={port0}",
        "v4l2src", "device=/dev/video2",
        "!", "video/x-raw,width=640,height=480,framerate=30/1",
        "!", "videoconvert",
        "!", "x264enc", "tune=zerolatency", "bitrate=500",
        "!", "rtph264pay", "config-interval=1", "pt=96",
        "!", "udpsink", f"host={host}", f"port={port1}"
    ]



    try:
        # Print starting message
        print(f"Starting dual-camera stream to {host}:{port0} and {host}:{port1}...")

        # Run the GStreamer pipeline
        subprocess.run(gst_command, check=True)

    except FileNotFoundError:
        # Handle case where GStreamer is not installed or accessible
        print("Error: GStreamer is not installed or `gst-launch-1.0` is not available in PATH.")

    except subprocess.CalledProcessError as e:
        # Handle errors from the GStreamer pipeline execution
        print(f"Error: GStreamer pipeline failed with return code {e.returncode}.")
        print("Check the pipeline configuration and ensure devices are available.")

    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error occurred: {e}")

    else:
        # Execute if no exceptions are raised
        print("Streaming started successfully.")

    finally:
        # Final cleanup or exit message
        print("Exiting the script. Ensure proper cleanup if required.")


if __name__ == "__main__":
    jetson_nano_ip = "100.71.196.8"  # Target IP address for streaming
    port0 = 5000
    port1 = 5001

    # Start the dual-camera stream
    start_dual_camera_stream(jetson_nano_ip, port0, port1)
