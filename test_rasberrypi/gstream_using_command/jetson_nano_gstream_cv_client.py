import cv2

def start_gstreamer_receiver(port: int):
    # GStreamer pipeline with appsink for OpenCV
    gst_pipeline = (
        f"udpsrc port={port} ! "
        "application/x-rtp, payload=96 ! "
        "rtph264depay ! "
        "avdec_h264 ! "
        "videoconvert ! "
        "appsink"
    )

    # Open the GStreamer pipeline with OpenCV
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Error: Unable to open GStreamer pipeline.")
        return

    print(f"Receiver pipeline started on port {port}. Press 'q' to quit.")

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame from GStreamer pipeline.")
                break

            # Display the frame using OpenCV
            cv2.imshow("Received Video Stream", frame)

            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        print("Receiver pipeline stopped.")
        cap.release()
        cv2.destroyAllWindows()
        
         # Kill any lingering GStreamer processes and capture errors
        result = subprocess.run(
            ["pkill", "-f", "gst-launch-1.0"],
            stderr=subprocess.PIPE,
            text=True  # To handle output as a string
            )
            
        if result.stderr:
            print("Error during cleanup with `pkill`:\n", result.stderr)
        else:
            print("GStreamer processes cleaned up successfully.\n")
        

# Example usage
if __name__ == "__main__":
    receiver_port = 5000  # The port number must match the sender
    start_gstreamer_receiver(receiver_port)
