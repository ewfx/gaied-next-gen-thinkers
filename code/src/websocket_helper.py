import os
from dotenv import load_dotenv
import json
import asyncio
import websockets
from database import *

# Load environment variables from .env file
load_dotenv()
storage = SRMemoryStorage()
connected_clients = set()

async def send_storage_data(websocket):
    """Sends the current storage data to a specific WebSocket client."""
    try:
        data = json.dumps({"type": "storage_data", "payload": storage.get_all_ticket_data()}, indent=4)
        await websocket.send(data)
        print(f"Storage data sent to client: {websocket.remote_address}")
    except websockets.exceptions.ConnectionClosedError:
        print(f"Connection closed for client: {websocket.remote_address}")
        connected_clients.discard(websocket)
    except Exception as e:
        print(f"Error sending storage data: {e}")

async def send_new_email_event():
    """Sends an event to all connected clients when a new email is received."""
    if connected_clients:
        message = json.dumps({"type": "new_email_received"})
        await asyncio.wait([client.send(message) for client in connected_clients])
        print("New email event sent to all clients.")
    else:
        print("No connected clients to send new email event to.")

async def send_classification_started_event(ticket_number):
    """Sends an event to all connected clients when classification starts."""
    if connected_clients:
        message = json.dumps({"type": "classification_started", "ticket_number": ticket_number})
        await asyncio.wait([client.send(message) for client in connected_clients])
        print(f"Classification started event sent for ticket: {ticket_number}")
    else:
        print(f"No connected clients to send classification started event for ticket: {ticket_number}.")

async def send_classification_data(ticket_number, classification_data):
    """Sends the classification data to all connected clients."""
    if connected_clients:
        message = json.dumps({"type": "classification_data", "ticket_number": ticket_number, "payload": classification_data}, indent=4)
        await asyncio.wait([client.send(message) for client in connected_clients])
        print(f"Classification data sent for ticket: {ticket_number}")
    else:
        print(f"No connected clients to send classification data for ticket: {ticket_number}.")

async def websocket_handler(websocket):
    """Handles WebSocket connections and messages."""
    connected_clients.add(websocket)
    print(f"Client connected: {websocket.remote_address}")
    await send_storage_data(websocket)  # Send storage data to the new client
    try:
        async for message in websocket:
            if message == "get_storage_data":
                await send_storage_data(websocket)
    except websockets.exceptions.ConnectionClosedError:
        print(f"Connection closed for client: {websocket.remote_address}")
    except websockets.exceptions.ConnectionClosedOK:
        print(f"Client disconnected gracefully: {websocket.remote_address}")
    finally:
        connected_clients.discard(websocket)
