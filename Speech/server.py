import asyncio
import websockets
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

async def websocket_handler(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            await websocket.send(f"Received: {message}")
        except websockets.exceptions.ConnectionClosed:
            break

def run_http_server():
    server = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    server.serve_forever()

def start_servers():
    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # Start WebSocket server
    return websockets.serve(websocket_handler, 'localhost', 8000)
