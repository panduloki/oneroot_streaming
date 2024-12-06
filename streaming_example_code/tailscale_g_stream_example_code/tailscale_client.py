import cv2

def stream_rtsp(rtsp_url):
    # Open the RTSP stream
    cap = cv2.VideoCapture(rtsp_url)

    # Check if the video stream is opened successfully
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    print("Connected to the stream.")

    # Read and display frames from the stream
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the frame in a window
        cv2.imshow('RTSP Stream', frame)

        # Press 'q' to exit the loop and close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting stream.")
            break

    # Release the capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Replace it with the Tailscale IP of the server and the stream URL
    tailscale_ip = "100.x.x.x"  # Replace it with actual Tailscale IP
    rtsp_url = f"rtsp://{tailscale_ip}:8554/test"

    # Start the RTSP stream
    stream_rtsp(rtsp_url)
