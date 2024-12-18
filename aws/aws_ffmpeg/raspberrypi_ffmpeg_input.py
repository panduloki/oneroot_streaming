import subprocess
import signal
import sys

# Global variable to store the FFmpeg process
ffmpeg_process = None


def handle_sigint(signum, frame):
    """Handle Ctrl+C to gracefully terminate the FFmpeg process."""
    global ffmpeg_process
    print("Gracefully stopping the sender...")
    if ffmpeg_process:
        ffmpeg_process.terminate()  # Send SIGTERM to FFmpeg
        ffmpeg_process.wait()  # Wait for FFmpeg to clean up
    sys.exit(0)


def start_sender(receiver_ip, port):
    global ffmpeg_process
    """ffmpeg -f v4l2 -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency -f mpegts udp://192.168.1.100:9999"""
    """ffmpeg -f v4l2 -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency -r 30 -s 640x480 -f mpegts udp://<receiver_ip>:<port>"""
    # FFmpeg command for streaming video
    command = [
        "ffmpeg",
        "-f", "v4l2", "-i", "/dev/video0",  # Capture video from webcam
        "-c:v", "libx264", "-preset", "ultrafast",  # Encode with H.264 for low latency
        "-tune", "zerolatency",
        "-f", "mpegts",  # Format for streaming
        f"udp://{receiver_ip}:{port}"  # Replace it with receiver's IP and port
    ]

    new_command = [
        "ffmpeg",
        "-f", "v4l2", "-i", "/dev/video0",  # Capture video from webcam
        "-c:v", "libx264",  # Encode video using H.264 codec
        "-preset", "ultrafast",  # Use ultrafast preset for low latency
        "-tune", "zerolatency",  # Tune encoder for zero latency
        "-r", "30",  # Set frame rate to 30 FPS
        "-s", "640x480",  # Set resolution to 640x480 to reduce bandwidth
        "-max_delay", "0",  # Reduce buffering delay
        "-rtbufsize", "100M",  # Set real-time buffer size to handle bursty traffic
        "-f", "mpegts",  # Format the output as MPEG-TS
        f"udp://{receiver_ip}:{port}"  # Stream to receiver using UDP
    ]

    try:
        ffmpeg_process = subprocess.Popen(new_command)
        ffmpeg_process.wait()  # Wait for FFmpeg to finish
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Sender stopped.")
        


if __name__ == "__main__":
    local_ip = "localhost"

    # Server IP variable
    jetson_nano_ip = "100.71.196.8"
    raspberrypi_ip = "100.126.63.67"
    msi_ip = "100.72.146.99"
    aws_ip = "100.97.35.29"

    port = 9000
    signal.signal(signal.SIGINT, handle_sigint)  # Set up signal handler
    start_sender(aws_ip, port)
