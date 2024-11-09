import cv2

# Define the Jetson Nano's local IP address
jetson_ip = "192.168.1.100"  # Replace this with the actual IP address of your Jetson Nano
rtsp_url = f"rtsp://{jetson_ip}:8554/test"

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
