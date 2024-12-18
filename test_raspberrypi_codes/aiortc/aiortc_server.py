import cv2
import asyncio
import json
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaPlayer
from aiohttp import web
from av import VideoFrame
import numpy as np
import time

# Video Stream Track for capturing and resizing frames
class CameraVideoTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)  # Open the first available camera (use appropriate index if needed)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")
        self.frame_rate = 15  # Limit to 15 frames per second
        self.frame_interval = 1 / self.frame_rate
        self.last_frame_time = time.time()

    async def recv(self):
        # Capture frame from camera
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture frame from camera")

        # Resize the frame to 640x480 (adjustable)
        frame_resized = cv2.resize(frame, (640, 480))

        # Limit frame rate
        if time.time() - self.last_frame_time >= self.frame_interval:
            # Convert to RGB
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            video_frame = VideoFrame.from_ndarray(frame_rgb, format="rgb24")
            video_frame.pts = video_frame.time_base * self.cap.get(cv2.CAP_PROP_POS_MSEC)
            video_frame.time_base = 1 / 1000  # 1000 ms in a second
            self.last_frame_time = time.time()
            return video_frame
        else:
            # Skip frame to maintain frame rate
            return await self.recv()

    def __del__(self):
        self.cap.release()


# WebRTC signaling offer handler
async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pc.addTrack(CameraVideoTrack())

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )


# Set up the web application to handle signaling requests
app = web.Application()
app.router.add_post("/offer", offer)

# Start the server on port 8080
if __name__ == "__main__":
    web.run_app(app, port=8080)
