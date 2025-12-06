"""
Dashboard integration with WebSocket real-time updates
"""
import asyncio
import websockets
import json
from loguru import logger
from datetime import datetime

class WebSocketDashboardClient:
    """WebSocket client for real-time dashboard updates"""
    
    def __init__(self, uri="ws://localhost:8765"):
        self.uri = uri
        self.websocket = None
        self.connected = False
        self.data_buffer = []
        
    async def connect(self):
        """Connect to WebSocket server"""
        try:
            self.websocket = await websockets.connect(self.uri)
            self.connected = True
            logger.info(f"Connected to WebSocket server at {self.uri}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket: {e}")
            self.connected = False
            return False
    
    async def listen(self, callback=None):
        """Listen for incoming messages"""
        if not self.websocket or not self.connected:
            await self.connect()
        
        try:
            async for message in self.websocket:
                data = json.loads(message)
                
                if data.get('type') == 'connected':
                    logger.info(f"Server message: {data.get('message')}")
                
                elif data.get('type') == 'volatility_update':
                    self.data_buffer.append(data)
                    logger.info(f"Received volatility update: {data.get('data', {}).get('volatility', 'N/A'):.4f}")
                    
                    # Call callback if provided
                    if callback:
                        await callback(data)
                
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket connection closed")
            self.connected = False
        except Exception as e:
            logger.error(f"Listen error: {e}")
            self.connected = False
    
    async def send(self, message: dict):
        """Send message to server"""
        if self.websocket and self.connected:
            try:
                await self.websocket.send(json.dumps(message))
            except Exception as e:
                logger.error(f"Send error: {e}")
    
    async def disconnect(self):
        """Disconnect from server"""
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            logger.info("Disconnected from WebSocket server")
    
    def get_latest_data(self):
        """Get latest data from buffer"""
        if self.data_buffer:
            return self.data_buffer[-1]
        return None
    
    def get_data_history(self, limit=10):
        """Get last N data points"""
        return self.data_buffer[-limit:]

# Example usage for Dash callback integration
async def dashboard_ws_callback(data):
    """Callback function for dashboard updates"""
    logger.info(f"Dashboard update: {data.get('timestamp')}")
    # Update Dash stores here with data

if __name__ == "__main__":
    async def main():
        client = WebSocketDashboardClient()
        await client.connect()
        await client.listen(callback=dashboard_ws_callback)
    
    asyncio.run(main())
