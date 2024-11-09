import cv2

def main():
    cap = cv2.VideoCapture("rtsp://localhost:8554/test")

    if not cap.isOpened():
        print("Error: Cannot open RTSP stream")
        return

    print("RTSP stream opened successfully")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Cannot read from stream")
            break

        cv2.imshow("RTSP Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()