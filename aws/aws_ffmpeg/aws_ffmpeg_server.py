import cv2
import signal
import sys
# start this code first
# Global variable to store the VideoCapture object
cap = None


def handle_sigint(signum, frame):
    """Handle Ctrl+C to gracefully release resources."""
    global cap
    print("Gracefully stopping the receiver...")
    if cap:
        cap.release()  # Release the video stream
    cv2.destroyAllWindows()  # Close OpenCV windows
    sys.exit(0)


def start_receiver(port):
    global cap
    """ffplay udp://:port"""
    stream_url = f"udp://0.0.0.0:{port}"  # Listen on UDP port 9999

    # Open the video stream
    cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)  # Reduce buffer size to minimize latency
    if not cap.isOpened():
        print("Error: Unable to open video stream.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read frame.")
                break

            # Process the frame (e.g., display or analyze it)
            #cv2.imshow("Receiver - Stream", frame)

            if frame is not None and frame.size > 0:
                print("frame received size: ", frame.shape)

            # Quit the stream by pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"Error while receiving stream: {e}")
    finally:
        print("Receiver stopped.")
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_sigint)  # Set up signal handler
    port1 = 9000
    start_receiver(port1)
