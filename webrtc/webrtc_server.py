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

            # Display the received frame
            cv2.imshow("Received Video", frame)

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


# Start the WebSocket server
async def main():
    try:
        server = await websockets.serve(handle_client, "0.0.0.0", 8765)
        print("Server running on ws://0.0.0.0:8765")
        await server.wait_closed()
    except Exception as e:
        print(f"Server error: {e}")


# Run the server
asyncio.run(main())
