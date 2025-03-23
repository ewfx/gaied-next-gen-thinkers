import asyncio
import websockets
import json
from datetime import datetime

async def websocket_listener():
    uri = "ws://localhost:8765"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to WebSocket server at {uri}")
            
            # Subscribe to all channels
            await websocket.send(json.dumps({"type": "subscribe", "channel": "storage"}))
            await websocket.send(json.dumps({"type": "subscribe", "channel": "events"}))
            await websocket.send(json.dumps({"type": "subscribe", "channel": "classification"}))
            print("Subscribed to all channels (storage, events, classification)\n")
            
            while True:
                message = await websocket.recv()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data = json.loads(message)
                
                print(f"[{timestamp}] Received message:")
                print(json.dumps(data, indent=2))
                print("-" * 60)
                
    # except websockets.exceptions.ConnectionClosed:
    #     print("Connection closed by server")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Starting WebSocket listener...")
    asyncio.get_event_loop().run_until_complete(websocket_listener())