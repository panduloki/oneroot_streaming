import asyncio
import websockets
import psutil
import json
import time

async def status_handler(websocket, path):
    try:
        async for message in websocket:
            if message == "get_status":
                status = {
                    "cpu_usage": psutil.cpu_percent(interval=1),
                    "memory": psutil.virtual_memory()._asdict(),
                    "temperature": get_temperature(),
                    "uptime": time.time() - psutil.boot_time()
                }
                await websocket.send(json.dumps(status))
            elif message == "ping":
                await websocket.send("Pong")
            else:
                await websocket.send("Unknown command")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed by the client.")

def get_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return float(f.read()) / 1000.0
    except FileNotFoundError:
        return None

# Start the WebSocket server
start_server = websockets.serve(status_handler, "0.0.0.0", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server running on ws://0.0.0.0:8765")
asyncio.get_event_loop().run_forever()

