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
    # FFmpeg command for streaming video
    command = [
        "ffmpeg",
        "-f", "v4l2", "-i", "/dev/video0",  # Capture video from webcam
        "-c:v", "libx264", "-preset", "ultrafast",  # Encode with H.264 for low latency
        "-tune", "zerolatency",
        "-f", "mpegts",  # Format for streaming
        f"udp://{receiver_ip}:{port}"  # Replace it with receiver's IP and port
    ]

    try:
        ffmpeg_process = subprocess.Popen(command)
        ffmpeg_process.wait()  # Wait for FFmpeg to finish
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Sender stopped.")


if __name__ == "__main__":

    signal.signal(signal.SIGINT, handle_sigint)  # Set up signal handler
    start_sender()
