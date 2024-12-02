import cv2
import asyncio
import websockets
import base64

async def send_frames(websocket, path):
    cap = cv2.VideoCapture(0)  # Open the webcam
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)  # Encode frame as JPEG
        frame_data = base64.b64encode(buffer).decode('utf-8')  # Base64 encode the frame
        await websocket.send(frame_data)  # Send the frame

        await asyncio.sleep(0.033)  # Stream at ~30 FPS

    cap.release()

# Server IP variable
aws_ip = "100.97.35.29"

start_server = websockets.serve(send_frames, aws_ip, 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
