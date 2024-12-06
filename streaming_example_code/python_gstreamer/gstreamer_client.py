import cv2

server_ip_address = "100.71.196.8"
def main():
    # Define the RTSP URL (replace with your server's public IP or domain name if on WAN)
    rtsp_url = f"rtsp://{server_ip_address}:8554/test"  # Replace <public_ip_or_domain>

    try:
        # Try to open the RTSP stream
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            raise Exception("Cannot open RTSP stream")

        print("RTSP stream opened successfully")

        # Read and display frames from the RTSP stream
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Cannot read from stream or connection lost")
                break

            cv2.imshow("RTSP Stream", frame)

            # Press 'q' to exit the stream display
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting stream display")
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Release the capture and close display windows
        cap.release()
        cv2.destroyAllWindows()
        print("Resources released, windows closed")

if __name__ == "__main__":
    main()
