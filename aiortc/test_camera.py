import cv2

def test_camera():
    # Open the default camera (0 for the first camera, 1 for the second, etc.)
    cap = cv2.VideoCapture(0)  # Change 0 to 1 if using a USB camera or try other indexes
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    print("Press 'q' to quit the video feed.")
    
    # Capture frames continuously from the camera
    while True:
        ret, frame = cap.read()  # Read a frame from the camera
        if not ret:
            print("Error: Failed to capture image.")
            break
        
        # Display the resulting frame
        cv2.imshow("Camera Feed", frame)
        
        # Exit the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Run the camera test
if __name__ == "__main__":
    test_camera()
