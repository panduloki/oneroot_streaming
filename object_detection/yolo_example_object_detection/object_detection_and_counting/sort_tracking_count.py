import os
import cv2
import numpy as np
from sort.sort import Sort  # Import Sort from the local sort.py file
from ultralytics import YOLO

try:
    # Initialize YOLOv8 model
    print("YOLOv8 model initialising .......")
    model = YOLO("yolo-Weights/yolov8n.pt")  # Path to your YOLOv8 weights file
    print("YOLOv8 model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLOv8 model: {e}")
    exit(1)

# Object Classes for YOLOv8 (COCO dataset)
classNames = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog",
    "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
    "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot",
    "hot dog", "pizza", "donut", "cake", "chair", "sofa", "potted plant", "bed", "dining table",
    "toilet", "tv monitor", "laptop", "mouse", "remote", "keyboard", "mobile phone", "microwave",
    "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear",
    "hair dryer", "toothbrush"
]

# Initialize SORT tracker
try:
    tracker = Sort()
except Exception as e:
    print(f"Error initializing SORT tracker: {e}")
    exit(1)


# Define a video path
video_path = os.path.join(os.getcwd(), "sample_video", "walk.mp4")
# Set video resolution
width, height = 1280, 720
try:
    # Verify if the video file exists
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file does not exist: {video_path}")

    # Initialize video capture
    cap = cv2.VideoCapture(video_path)

    # Check if video capture is successfully opened
    if not cap.isOpened():
        raise Exception(f"Unable to open video file at video_path: {video_path}")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    print(f"Video capture initialized successfully: {video_path}")
    print(f"Resolution set to: {width}x{height}")

except FileNotFoundError as fnf_error:
    print(f"File error: {fnf_error}")
    exit(1)
except Exception as e:
    print(f"Error initializing video capture: {e}")
    exit(1)

# Initialize a set to store unique track IDs that cross the middle box
unique_ids_crossed = set()
try:
    while True:
        success, img = cap.read()
        if not success:
            print("End of video or failed to read frame.")
            break

        # Resize and define middle box dimensions
        img = cv2.resize(img, (1280, 720))
        height, width, _ = img.shape
        middle_box_x1 = width // 4
        middle_box_y1 = height // 4
        middle_box_x2 = 3 * width // 4
        middle_box_y2 = 3 * height // 4

        # Run YOLOv8 detection
        results = model(img, stream=True)

        detections = []

        # Extract detections from YOLOv8 results
        for r in results:
            boxes = r.boxes  # Detected boxes
            for box in boxes:
                # Extract bounding box and class info
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                class_id = int(box.cls[0])
                confidence = box.conf[0].cpu().numpy()

                # Track only specific classes (e.g., person, car, etc.)
                if class_id in [0, 1, 2, 3, 4]:
                    detections.append([x1, y1, x2, y2, confidence])

        # Update SORT tracker with detections
        if len(detections) > 0:
            detections = np.array(detections)
            trackers = tracker.update(detections)

            # Draw tracking results and check for crossings
            for track in trackers:
                x1, y1, x2, y2, track_id = track.astype(int)

                # Calculate the centroid of the bounding box
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                # Check if centroid is within the middle box
                if middle_box_x1 < cx < middle_box_x2 and middle_box_y1 < cy < middle_box_y2:
                    # Only add track_id if it hasn't been counted already
                    if track_id not in unique_ids_crossed:
                        unique_ids_crossed.add(track_id)

                # Draw bounding box and ID on frame
                label = f"ID: {track_id}"
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        # Draw middle box and display crossing count
        cv2.rectangle(img, (middle_box_x1, middle_box_y1), (middle_box_x2, middle_box_y2), (0, 0, 255), 2)
        cv2.putText(img, f"Crossed: {len(unique_ids_crossed)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        # Display the frame
        cv2.imshow("Object Detection and Tracking", img)

        # Exit loop if 'ESC' key is pressed
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:  # ESC key
            print("user pressed q or exit key")
            break
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Release resources and close all OpenCV windows
    if 'cap' in locals() and cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    print("Resources released and application closed.")
