from ultralytics import YOLO
import cv2
import numpy as np
from collections import defaultdict

# Start Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1080)
cap.set(4, 720)

# YOLO Model
model = YOLO("yolo-Weights/yolov8n.pt")

# Object Classes
classNames = ["Person", "Bicycle", "Car", "Motorbike", "Aeroplane", "Bus", "Train", "Truck", "Boat",
              "Traffic Light", "Fire Hydrant", "Stop Sign", "Parking Meter", "Bench", "Bird", "Cat",
              "Dog", "Horse", "Sheep", "Cow", "Elephant", "Bear", "Zebra", "Giraffe", "Backpack", "Umbrella",
              "Handbag", "Tie", "Suitcase", "Frisbee", "Skis", "Snowboard", "Sports Ball", "Kite", "Baseball Bat",
              "Baseball Glove", "Skateboard", "Surfboard", "Tennis Racket", "Bottle", "Wine Glass", "Cup",
              "Fork", "Knife", "Spoon", "Bowl", "Banana", "Apple", "Sandwich", "Orange", "Broccoli",
              "Carrot", "Hot dog", "Pizza", "Donut", "Cake", "Chair", "Sofa", "Potted Plant", "Bed",
              "Dining Table", "Toilet", "TV Monitor", "Laptop", "Mouse", "Remote", "Keyboard", "Mobile Phone",
              "Microwave", "Oven", "Toaster", "Sink", "Refrigerator", "Book", "Clock", "Vase", "Scissors",
              "Teddy Bear", "Hair Dryer", "Toothbrush"
              ]

# Object tracking state
object_tracker = defaultdict(list)  # To track objects with their previous positions
crossed_ids = set()  # To avoid double counting

# Dynamically calculate boundary rectangle
height, width = 720, 1080
boundary_top_left = (width // 4, height // 4)  # 1/4 width and height
boundary_bottom_right = (3 * width // 4, 3 * height // 4)  # 3/4 width and height


object_count = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip camera horizontally
    results = model(img, stream=True)



    for r in results:
        boxes = r.boxes

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Compute center of bounding box (centroid)
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            # Draw centroid
            cv2.circle(img, (center_x, center_y), 5, (0, 255, 255), -1)

            # Assign colors based on confidence
            confidence = round(float(box.conf[0]) * 100, 2)
            color = (0, 255, 0) if confidence > 95 else (0, 0, 255)

            # Draw bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

            # Draw confidence and class name
            class_index = int(box.cls[0])
            class_name = classNames[class_index]
            text = f"{class_name}: {confidence}%"
            org = (x1, y1 - 10)
            cv2.putText(img, text, org, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Draw ID at the top-right of the bounding box
            obj_id = box.id
            cv2.putText(img, f"ID: {obj_id}", (x2 - 50, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

            # Update tracking state
            object_tracker[obj_id].append((center_x, center_y))

            # Check if the object crosses the boundary
            if len(object_tracker[obj_id]) > 1:
                prev_x, prev_y = object_tracker[obj_id][-2]
                if (boundary_top_left[0] <= prev_x <= boundary_bottom_right[0] and
                        boundary_top_left[1] <= prev_y <= boundary_bottom_right[1]):
                    if obj_id not in crossed_ids:
                        object_count += 1
                        crossed_ids.add(obj_id)

    # Draw the rectangular boundary
    cv2.rectangle(img, boundary_top_left, boundary_bottom_right, (255, 255, 0), 2)
    cv2.putText(img, f"Count: {object_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Object Detection and Counting", img)
    if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()
