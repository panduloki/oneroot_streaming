import cv2
import asyncio
import websockets

# Server IP variable
jetson_nano_ip = "100.71.196.8"  # Replace it with your server's IP address
raspberrypi_ip = "100.126.63.67"
msi_ip = "100.72.146.99"


# Replace it with the server's IP address
server_ip = msi_ip # send video to this ip
server_port = 8765
SERVER_URL = f"ws://{server_ip}:{server_port}"


async def send_video():
    """
    Captures frames from the camera and sends them to the server.
    """
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            print("Connected to the server.")

            # Open the camera
            capture = cv2.VideoCapture(0)
            if not capture.isOpened():
                print("Error: Unable to access the camera.")
                return

            while True:
                # Capture a frame from the camera
                ret, frame = capture.read()
                if not ret:
                    print("Failed to capture frame. Exiting...")
                    break

                # Resize and encode the frame as JPEG
                frame = cv2.resize(frame, (640, 480))  # Resize for consistent performance
                _, buffer = cv2.imencode('.jpg', frame)

                # Send the encoded frame to the server
                await websocket.send(buffer.tobytes())

                # Display the local video for confirmation
                cv2.imshow("Sending Video", frame)

                # Exit if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Cleanup
            capture.release()
            cv2.destroyAllWindows()

    except websockets.ConnectionError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# Run the client
if __name__ == "__main__":
    try:
        asyncio.run(send_video())
    except KeyboardInterrupt:
        print("\nClient stopped.")
    except Exception as e:
        print(f"Critical error: {e}")
