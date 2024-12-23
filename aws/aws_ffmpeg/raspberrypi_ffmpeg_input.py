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

def build_ffmpeg_command(receiver_ip, port):
    """Build the FFmpeg command for streaming video."""
    return [
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

def start_sender(receiver_ip, port):
    global ffmpeg_process
    command = build_ffmpeg_command(receiver_ip, port)
    try:
        ffmpeg_process = subprocess.Popen(command)
        ffmpeg_process.wait()  # Wait for FFmpeg to finish
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Sender stopped.")

if __name__ == "__main__":
    aws_ip = "100.97.35.29"
    port = 9000
    signal.signal(signal.SIGINT, handle_sigint)  # Set up signal handler
    start_sender(aws_ip, port)
