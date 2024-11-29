import cv2
import socket
import logging
import threading
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
def receive_stream(host, port):
    """
    Receives an RTP video stream from the given host and port, decodes it, and displays it.
    Args:
        host (str): The IP address of the stream source.
        port (int): The port number of the stream source.
    """
    logger.info(f"Setting up video stream client for {host}:{port}")
    # Create an OpenCV VideoCapture using the GStreamer pipeline
    gst_pipeline = (
        f"udpsrc port={port} ! "
        f"application/x-rtp,encoding-name=H264,payload=96 ! "
        f"rtph264depay ! "
        f"h264parse ! "
        f"avdec_h264 ! "
        f"videoconvert ! "
        f"appsink sync=false"
    )
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        logger.error(f"Failed to open the video stream on {host}:{port}")
        return
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.warning(f"Failed to receive frame from {host}:{port}")
                break
            # Display the video frame
            cv2.imshow(f"Video Stream - {port}", frame)
            # Break on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logger.info(f"Exiting video stream display for {host}:{port}")
                break
    except Exception as e:
        logger.error(f"Error receiving stream from {host}:{port}: {e}")
    finally:
        # Clean up resources
        cap.release()
        cv2.destroyWindow(f"Video Stream - {port}")
        logger.info(f"Stopped receiving video stream on {host}:{port}")
if __name__ == "__main__":
    # Define the host IP and ports to receive video streams
    # server_ip = "100.71.196.8"  # IP of the server sending the streams
    ports = [5000, 5001]  # Corresponding ports for the two streams
    # Create threads for each video stream
    threads = []
    try:
        for port in ports:
            t = threading.Thread(target=receive_stream, args=("0.0.0.0", port))
            threads.append(t)
            t.start()
        # Wait for all threads to complete
        for t in threads:
            t.join()
    except Exception as e:
        logger.error(f"Error occurred while setting up video streams: {e}")
    finally:
        logger.info("All video streams stopped. Exiting...")