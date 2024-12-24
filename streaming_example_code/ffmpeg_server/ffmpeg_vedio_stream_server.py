import subprocess
import time
import threading
import os

class RTSPServer:
    def __init__(self, stream_url='rtsp://localhost:8554/stream', video_device='/dev/video0', audio_device=None):
        self.stream_url = stream_url
        self.video_device = video_device
        self.audio_device = audio_device
        self.ffmpeg_process = None
        self.is_paused = False
        self.is_running = True

    def start_stream(self):
        """Start streaming the video with FFmpeg."""
        command = [
            'ffmpeg',
            '-f', 'v4l2',  # Video capture format
            '-i', self.video_device,  # Video input from USB camera
            '-f', 'alsa',  # Audio capture format (if an audio device is provided)
            '-i', self.audio_device if self.audio_device else 'dummy',  # Audio input (optional)
            '-c:v', 'libx264',  # Video codec
            '-c:a', 'aac',  # Audio codec (if applicable)
            '-preset', 'fast',  # Video encoding speed
            '-f', 'rtsp',  # Output format
            self.stream_url  # RTSP stream URL
        ]

        self.ffmpeg_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        threading.Thread(target=self._read_output(command=command), daemon=True).start()
        print("Streaming started...")

    def _read_output(self, command):
        """Read the output and error streams of the FFmpeg process."""
        while self.ffmpeg_process and self.ffmpeg_process.poll() is None:
            output = self.ffmpeg_process.stdout.readline()
            if output:
                print(f"output of ffmpeg_process command {command}: {output.decode().strip()}")
            error = self.ffmpeg_process.stderr.readline()
            if error:
                print(f"error of ffmpeg_process command {command}: {error.decode().strip()}")
        
    def stop_stream(self):
        """Stop the streaming process."""
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()
            self.ffmpeg_process = None
            print("FFmpeg Streaming stopped.")
        
    def pause_stream(self):
        """Pause the streaming by terminating FFmpeg."""
        if not self.is_paused and self.ffmpeg_process:
            self.ffmpeg_process.send_signal(subprocess.signal.SIGSTOP)  # Send SIGSTOP to pause the process
            self.is_paused = True
            print("FFmpeg Streaming paused.")
        
    def resume_stream(self):
        """Resume the streaming by restarting FFmpeg."""
        if self.is_paused and self.ffmpeg_process:
            self.ffmpeg_process.send_signal(subprocess.signal.SIGCONT)  # Send SIGCONT to resume
            self.is_paused = False
            print("FFmpeg Streaming Streaming resumed.")
        
    def seek_stream(self, seek_time='00:01:00'):
        """Seek to a specific timestamp in the video stream."""
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()
            print(f"Seeking to {seek_time}...")
            self.start_stream()

    def restart_stream(self):
        """Restart the stream after a pause or seek."""
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()
        self.start_stream()

# Example of usage
if __name__ == '__main__':
    rtsp_server = RTSPServer()

    # Start the stream
    rtsp_server.start_stream()

    # Simulate controls
    #time.sleep(10)  # Stream for 10 seconds
    #rtsp_server.pause_stream()  # Pause the stream
    #time.sleep(5)  # Wait for 5 seconds before resuming
    #rtsp_server.resume_stream()  # Resume streaming
    #time.sleep(5)
    #rtsp_server.seek_stream('00:01:00')  # Seek to 1 minute into the stream
    time.sleep(5000)
    rtsp_server.stop_stream()  # Stop the stream
