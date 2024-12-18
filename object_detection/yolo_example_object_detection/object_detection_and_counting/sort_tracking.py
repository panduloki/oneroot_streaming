import os
import cv2
import numpy as np
from sort.sort import Sort  # Import Sort from the local sort.py file

print("YOLOv8 model initialising .......")
from ultralytics import YOLO

try:
    # Initialize YOLOv8 model
    model = YOLO("yolo-Weights/yolov8n.pt")  # Path to your YOLOv8 weights file
    print("YOLOv8 model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLOv8 model: {e}")
    exit(1)

# Initialize SORT tracker
try:
    tracker = Sort()
except Exception as e:
    print(f"Error initializing SORT tracker: {e}")
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

    while True:
        success, img = cap.read()
        if not success:
            print("End of video or failed to read frame.")
            break

        img = cv2.resize(img, (1280, 720))

        # Run YOLOv8 detection
        try:
            results = model(img, stream=True)
        except Exception as e:
            print(f"Error during YOLOv8 inference: {e}")
            break

        detections = []
        confidences = []

        try:
            for r in results:
                boxes = r.boxes  # Detected boxes
                for box in boxes:
                    # Extract the bounding box (xyxy)
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()  # (x1, y1, x2, y2)
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # Get the class label and confidence score
                    class_id = int(box.cls[0])
                    confidence = box.conf[0].cpu().numpy()

                    # Only track certain classes
                    if class_id in [0, 1, 2, 3, 4]:  # e.g., person, car, bus, etc.
                        detections.append([x1, y1, x2, y2, confidence])
                        confidences.append(confidence)

                        # Draw bounding box and class name
                        label = classNames[class_id]
                        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv2.putText(img, f"{label}: {confidence:.2f}", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        except Exception as e:
            print(f"Error processing detection results: {e}")
            continue

        # Update the tracker if there are detections
        if len(detections) > 0:
            try:
                detections = np.array(detections)
                trackers = tracker.update(detections)
                for i, track in enumerate(trackers):
                    x1, y1, x2, y2, track_id = track.astype(int)
                    label = f"ID: {track_id}"
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            except Exception as e:
                print(f"Error updating tracker: {e}")

        # Display the frame with object detection and tracking
        cv2.imshow("Object Detection and Tracking", img)

        # Exit loop if 'ESC' key is pressed
        key = cv2.waitKey(1)
        if  key == ord('q') or key == 27:  # ESC key
            print("user pressed q or exit key")
            break
except Exception as e:
    print(f"Error in main loop: {e}")
except FileNotFoundError as fnf_error:
    print(f"File error: {fnf_error}")
finally:
    # Release the capture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
