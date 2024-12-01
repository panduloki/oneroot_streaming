import cv2

import os
os.environ['QT_QPA_PLATFORM'] = 'xcb'  # Force Qt to use X11

# Use the device path instead of the index
device_path = "/dev/video0"  # Adjust if your camera is at a different path

try:
    cap = cv2.VideoCapture(device_path)
    
    if not cap.isOpened():
        raise Exception(f"Cannot open camera at {device_path}")
    
    print("Press 'q' to exit the video window.")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # Check if the frame was captured successfully
        if not ret:
            print("Failed to grab frame")
            break
        
        # Display the frame
        cv2.imshow('USB Camera Test', frame)
        
        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error: {e}")

finally:
    # Release the camera and close all OpenCV windows
    if 'cap' in locals():
        cap.release()
    cv2.destroyAllWindows()
