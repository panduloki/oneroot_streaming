import cv2
import time

class RTSPClient:
    def __init__(self, server_ip='localhost', stream_port=8554, stream_name='stream'):
        # Use the provided server IP, port, and stream name to form the RTSP URL
        self.stream_url = f'rtsp://{server_ip}:{stream_port}/{stream_name}'
        self.capture = None
        self.is_paused = False

    def start_stream(self):
        """Start connecting to the RTSP stream."""
        self.capture = cv2.VideoCapture(self.stream_url)
        if not self.capture.isOpened():
            print("Failed to open stream.")
            return False
        print("Stream started.")
        return True

    def stop_stream(self):
        """Stop the video stream."""
        if self.capture.isOpened():
            self.capture.release()
            print("Stream stopped.")
        
    def pause_stream(self):
        """Pause the stream."""
        self.is_paused = True
        print("Stream paused.")

    def resume_stream(self):
        """Resume the stream."""
        self.is_paused = False
        print("Stream resumed.")

    def seek_stream(self, seek_time='00:01:00'):
        """Seek to a specific time in the stream."""
        if self.capture.isOpened():
            seconds = self.convert_time_to_seconds(seek_time)
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, seconds * self.capture.get(cv2.CAP_PROP_FPS))
            print(f"Seeking to {seek_time}...")
        
    def convert_time_to_seconds(self, time_str):
        """Convert a time string in 'HH:MM:SS' format to seconds."""
        h, m, s = map(int, time_str.split(":"))
        return h * 3600 + m * 60 + s

    def show_stream(self):
        """Display the stream frames."""
        while True:
            if self.is_paused:
                time.sleep(1)
                continue
            ret, frame = self.capture.read()
            if not ret:
                print("Stream ended or failed.")
                break
            cv2.imshow("RTSP Stream", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Press 'q' to quit
                break
            elif key == ord('p'):  # Press 'p' to pause
                self.pause_stream()
            elif key == ord('r'):  # Press 'r' to resume
                self.resume_stream()
            elif key == ord('s'):  # Press 's' to seek to 30 seconds
                self.seek_stream('00:00:30')

        self.stop_stream()
        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    server_ip = '192.168.1.10'  # Replace with the actual server IP
    rtsp_client = RTSPClient(server_ip=server_ip, stream_port=8554, stream_name='stream')

    if rtsp_client.start_stream():
        rtsp_client.show_stream()  # Start displaying the stream with controls
