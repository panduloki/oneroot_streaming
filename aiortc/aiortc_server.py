import cv2
import asyncio
import json
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole
from aiohttp import web
from av import VideoFrame


class CameraVideoTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)  # Adjust camera index if needed
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")

    async def recv(self):
        # Capture frame from camera
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture frame from camera")

        # Convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_frame = VideoFrame.from_ndarray(frame_rgb, format="rgb24")
        video_frame.pts = video_frame.time_base * self.cap.get(cv2.CAP_PROP_POS_MSEC)
        video_frame.time_base = 1 / 1000
        return video_frame

    def __del__(self):
        self.cap.release()


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


app = web.Application()
app.router.add_post("/offer", offer)

if __name__ == "__main__":
    web.run_app(app, port=8080)
