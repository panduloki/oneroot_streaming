import asyncio
import time

import websockets
import json
raspberrypi_ip = "100.126.63.67"
async def request_status():
    uri = f"ws://{raspberrypi_ip}:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("get_status")
        response = await websocket.recv()
        print("Received Status:", json.loads(response))

# Request status every 60 seconds
while True:
    asyncio.run(request_status())
    time.sleep(60)
