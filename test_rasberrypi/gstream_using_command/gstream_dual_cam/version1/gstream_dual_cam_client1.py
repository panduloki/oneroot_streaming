import cv2
import socket
import logging
import numpy as np

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
    # Create an UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    logger.info(f"Listening for video stream on {host}:{port}")

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
            cv2.imshow(f"Video Stream - {host}:{port}", frame)

            # Break on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logger.info(f"Exiting video stream display for {host}:{port}")
                break
    except Exception as e:
        logger.error(f"Error receiving stream from {host}:{port}: {e}")
    finally:
        # Clean up resources
        cap.release()
        cv2.destroyAllWindows()
        sock.close()
        logger.info(f"Stopped receiving video stream on {host}:{port}")


if __name__ == "__main__":
    # Define the host IP and ports to receive video streams
    server_ip = "100.71.196.8"  # Server IP address
    receiver_host = "0.0.0.0"  # Listen on all interfaces
    ports = [5000, 5001]  # Corresponding ports for the two streams
    try:
        # Launch clients to receive video streams for each port
        for port in ports:
            logger.info(f"Starting video stream client for {receiver_host}:{port}")
            receive_stream(receiver_host, port)

    except Exception as e:
        logger.error(f"Error to receive stream{e}")