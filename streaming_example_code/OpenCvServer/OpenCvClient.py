import cv2

def start_rtsp_client():
    # GStreamer pipeline to receive and display the RTSP stream
    gst_pipeline = (
        "udpsrc port=5000 ! "
        "application/x-rtp, payload=96 ! "
        "rtph264depay ! h264parse ! avdec_h264 ! "
        "videoconvert ! appsink"
    )

    # Open the stream using OpenCV with GStreamer pipeline
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print("Failed to open RTSP stream.")
        return

    print("Receiving video stream...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Display the frame
        cv2.imshow("RTSP Client", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_rtsp_client()
