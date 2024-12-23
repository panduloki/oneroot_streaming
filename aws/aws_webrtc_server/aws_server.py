import cv2
import asyncio
import websockets
import numpy as np


async def handle_client(websocket, path):
    """
    Handles incoming video frames from the client and displays them.
    """
    try:
        print(f"Client connected: {websocket.remote_address}")
        while True:
            # Receive the encoded frame data from the client
            frame_data = await websocket.recv()

            # Convert the byte data back into an image
            nparr = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if frame is None or frame.size == 0:
                print("Received an empty frame.")
                continue
            #print("frame received size: ", frame.shape)

            # Display the received frame
            # Uncomment the line below to display the received video frame for debugging purposes
            # cv2.imshow("Received Video", frame)

            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except websockets.ConnectionClosed:
        print(f"Connection closed: {websocket.remote_address}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cv2.destroyAllWindows()
        print(f"Connection with {websocket.remote_address} closed.")

async def main():
    """
    Starts the WebSocket server and waits for it to close.
    """
# Start the WebSocket server
async def main():
    try:
        server = await websockets.serve(handle_client, "127.0.0.1", 8765)
        print("Server running on ws://127.0.0.1:8765")
        await server.wait_closed()
    except Exception as e:
        print(f"Server error: {e}")


# Run the server
asyncio.run(main())
