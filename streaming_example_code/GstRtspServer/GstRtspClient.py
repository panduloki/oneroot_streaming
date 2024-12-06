import cv2

# Define the Jetson Nano's local IP address
jetson_ip = "100.65.5.95"  # Replace this with the actual IP address of your Jetson Nano
rtsp_url = f"udp://{jetson_ip}:5000"

# Open the RTSP stream
cap = cv2.VideoCapture(rtsp_url)

# Check if the stream was successfully opened
if not cap.isOpened():
    print("Error: Could not open RTSP stream.")
    exit()


# Display the RTSP stream
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the resulting frame
    cv2.imshow("RTSP Stream", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close the display window
cap.release()
cv2.destroyAllWindows()
