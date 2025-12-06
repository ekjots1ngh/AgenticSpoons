"""
WebSocket server for real-time data streaming
"""
import asyncio
import websockets
import json
from loguru import logger
from datetime import datetime

class AgentSpoonsWebSocketServer:
    """Real-time data streaming via WebSockets"""
    
    def __init__(self, host='0.0.0.0', port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        
    async def register(self, websocket):
        """Register new client"""
        self.clients.add(websocket)
        logger.info(f"Client connected. Total: {len(self.clients)}")
        
    async def unregister(self, websocket):
        """Unregister client"""
        self.clients.remove(websocket)
        logger.info(f"Client disconnected. Total: {len(self.clients)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all clients"""
        if self.clients:
            message_str = json.dumps(message)
            await asyncio.gather(
                *[client.send(message_str) for client in self.clients],
                return_exceptions=True
            )
    
    async def handler(self, websocket, path):
        """Handle client connection"""
        await self.register(websocket)
        
        try:
            # Send welcome message
            await websocket.send(json.dumps({
                'type': 'connected',
                'message': 'AgentSpoons WebSocket Server',
                'timestamp': datetime.now().isoformat()
            }))
            
            # Keep connection alive
            async for message in websocket:
                # Echo back for now
                await websocket.send(message)
                
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
    
    async def data_streamer(self):
        """Stream live data to all clients"""
        while True:
            try:
                # Load latest data
                with open('data/results.json', 'r') as f:
                    data = json.load(f)
                
                if data:
                    latest = data[-1]
                    
                    # Broadcast to all clients
                    await self.broadcast({
                        'type': 'volatility_update',
                        'data': latest,
                        'timestamp': datetime.now().isoformat()
                    })
                
                await asyncio.sleep(2)  # Stream every 2 seconds
                
            except Exception as e:
                logger.error(f"Stream error: {e}")
                await asyncio.sleep(5)
    
    async def start(self):
        """Start WebSocket server"""
        logger.info(f"WebSocket server starting on ws://{self.host}:{self.port}")
        
        # Start server
        async with websockets.serve(self.handler, self.host, self.port):
            # Start data streamer
            await self.data_streamer()

if __name__ == "__main__":
    server = AgentSpoonsWebSocketServer()
    asyncio.run(server.start())
