import cv2
import numpy as np

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1080)  # Set video width
cap.set(4, 720)   # Set video height

# Read the first frame
ret, frame = cap.read()
if not ret:
    print("Failed to read frame.")
    cap.release()
    exit()

# Convert the frame to grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Detect good features to track (corners) in the first frame
# Parameters: maxCorners (max number of corners), qualityLevel (minimum quality level of corners)
# minDistance (minimum distance between corners), blockSize (size of the window for corner detection)
corners = cv2.goodFeaturesToTrack(gray, mask=None, maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

# Create a mask image for drawing purposes
mask = np.zeros_like(frame)

# Initialize previous frame for optical flow calculation
prev_gray = gray.copy()

# Initialize the list to store previous feature points
prev_corners = corners

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the current frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate optical flow (KLT) - track the corners from previous frame to current frame
    new_corners, status, error = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_corners, None)

    # Select the good points (those for which tracking was successful)
    good_new = new_corners[status == 1]
    good_old = prev_corners[status == 1]

    # Draw the tracking lines and circles on the image
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()  # Flatten to single value
        c, d = old.ravel()  # Flatten to single value

        # Convert the points to integers before passing to cv2.line and cv2.circle
        a, b, c, d = int(a), int(b), int(c), int(d)

        # Draw a line between the old and new positions
        frame = cv2.line(frame, (a, b), (c, d), (0, 255, 0), 2)

        # Draw a circle at the new position
        frame = cv2.circle(frame, (a, b), 5, (0, 0, 255), -1)

    # Display the tracking result
    cv2.imshow("KLT Tracking", frame)

    # Update the previous frame and previous corners for the next iteration
    prev_gray = gray.copy()
    prev_corners = good_new.reshape(-1, 1, 2)

    # Exit the loop if 'ESC' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

# Release the capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
