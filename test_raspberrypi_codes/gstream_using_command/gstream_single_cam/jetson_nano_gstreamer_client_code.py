import subprocess
import cv2
import numpy as np

def start_gstreamer_receiver(host: str, port: int):
    # gst_command = [
    #     "gst-launch-1.0",
    #     "udpsrc", f"port={port}",
    #     "!", "application/x-rtp,encoding-name=H264",
    #     "!", "rtph264depay",
    #     "!", "avdec_h264",
    #     "!", "videoconvert",
    #     "!", "appsink"
    # ]

    gst_command = [
        "gst-launch-1.0", "-v",
        "udpsrc", f"port={port}",
        "!", "application/x-rtp,payload=96",
        "!", "rtph264depay",
        "!", "avdec_h264",
        "!", "videoconvert",
        "!", "xvimagesink"
    ]

    try:
        # Start the GStreamer pipeline and pipe the output to OpenCV using appsink
        process = subprocess.Popen(gst_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Receiver pipeline started on {host}:{port}")

        # Reading from GStreamer pipeline's output stream
        while True:
            # Capture the raw frame from the GStreamer pipeline
            output = process.stdout.read(1024)
            if output:
                # Convert the frame into a NumPy array and then to an OpenCV image
                nparr = np.frombuffer(output, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if frame is not None:
                    # Display the frame using OpenCV
                    cv2.imshow("Received Video Stream", frame)

                # Break loop on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
    except FileNotFoundError:
        print("GStreamer is not installed or `gst-launch-1.0` is not in PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Receiver pipeline stopped.")
        process.terminate()
        cv2.destroyAllWindows()
         
        # Kill any lingering GStreamer processes and capture errors
        result = subprocess.run(
            ["pkill", "-f", "gst-launch-1.0"],
            stderr=subprocess.PIPE,
            text=True  # To handle output as a string
            )
            
        if result.stderr:
            print("Error during cleanup with `pkill`:\n", result.stderr)
        else:
            print("GStreamer processes cleaned up successfully.\n")

# Example usage
if __name__ == "__main__":
    receiver_host = "0.0.0.0"  # Listen on all interfaces
    receiver_port = 5000       # The port number must match the sender
    start_gstreamer_receiver(receiver_host, receiver_port)
