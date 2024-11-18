import cv2
import asyncio
import json
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaPlayer
from aiohttp import ClientSession
from av import VideoFrame
import numpy as np

# Server IP variable
server_ip = "100.65.5.95"  # Replace with your server's IP address
server_port = 8080  # Port where the WebRTC server is running

class DummyVideoTrack(VideoStreamTrack):
    """
    A video track that provides blank frames.
    Needed to create an offer even without any real video source.
    """
    async def recv(self):
        # Create a blank black frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        video_frame = VideoFrame.from_ndarray(frame, format="bgr24")
        video_frame.pts = self.time_base * 1000
        video_frame.time_base = 1 / 30
        return video_frame

async def main():
    pc = RTCPeerConnection()
    dummy_track = DummyVideoTrack()
    pc.addTrack(dummy_track)

    async with ClientSession() as session:
        # Set up the connection with error handling
        async def connect():
            try:
                offer = await pc.createOffer()
                await pc.setLocalDescription(offer)
                async with session.post(
                    f"http://{server_ip}:{server_port}/offer",
                    json={"sdp": pc.localDescription.sdp, "type": pc.localDescription.type},
                ) as resp:
                    answer = await resp.json()
                    await pc.setRemoteDescription(
                        RTCSessionDescription(sdp=answer["sdp"], type=answer["type"])
                    )
                print("Connection established successfully.")
            except Exception as e:
                print(f"Error during connection setup: {e}")
                await pc.close()

        await connect()

        # Track for receiving video with error handling
        @pc.on("track")
        async def on_track(track):
            if track.kind == "video":
                print("Receiving video stream...")
                try:
                    while True:
                        frame = await track.recv()
                        img = frame.to_ndarray(format="bgr24")
                        cv2.imshow("WebRTC Stream", img)
                        if cv2.waitKey(1) & 0xFF == ord("q"):
                            break
                except Exception as e:
                    print(f"Error while receiving video: {e}")
                finally:
                    print("Stopping video stream...")
                    track.stop()

    # Close peer connection and destroy OpenCV windows
    await pc.close()
    try:
        cv2.destroyAllWindows()
    except cv2.error as e:
        print(f"Warning: Unable to close OpenCV windows: {e}")

asyncio.run(main())
