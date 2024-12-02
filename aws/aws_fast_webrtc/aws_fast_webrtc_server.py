import cv2
import asyncio
import websockets
import base64
import numpy as np

async def receive_frames():
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            try:
                # Receive frame data
                frame_data = await websocket.recv()
                # Decode the base64 frame
                frame_bytes = base64.b64decode(frame_data)
                nparr = np.frombuffer(frame_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                # Display the frame
                #cv2.imshow("WebRTC Frame", frame)

                if frame is not None and frame.size > 0:
                    print("frame received size: ", frame.shape)

                # Break on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break

        cv2.destroyAllWindows()

asyncio.get_event_loop().run_until_complete(receive_frames())
