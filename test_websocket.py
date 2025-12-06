"""
Test WebSocket server connectivity
"""
import asyncio
import websockets
import json
from loguru import logger
from src.api import WebSocketDashboardClient

async def test_websocket_connection():
    """Test connection to WebSocket server"""
    logger.info("Testing WebSocket server connection...")
    
    client = WebSocketDashboardClient()
    
    # Connect
    connected = await client.connect()
    if not connected:
        logger.error("Failed to connect to WebSocket server")
        logger.info("Make sure to run: python src/api/websocket_server.py")
        return False
    
    logger.info("✓ Connected to WebSocket server")
    
    # Send test message
    test_msg = {
        'type': 'test',
        'message': 'Hello from test client',
        'timestamp': asyncio.get_event_loop().time()
    }
    
    await client.send(test_msg)
    logger.info(f"✓ Sent test message")
    
    # Listen for a few messages
    logger.info("Listening for 5 messages...")
    
    message_count = 0
    async def listener_callback(data):
        nonlocal message_count
        message_count += 1
        logger.info(f"  Message {message_count}: {data.get('type')} - {data.get('timestamp')}")
        if message_count >= 5:
            await client.disconnect()
    
    try:
        await asyncio.wait_for(
            client.listen(callback=listener_callback),
            timeout=15
        )
    except asyncio.TimeoutError:
        logger.info("Timeout reached")
    except Exception as e:
        logger.error(f"Error: {e}")
    
    logger.info("✓ Test complete")
    return True

if __name__ == "__main__":
    try:
        result = asyncio.run(test_websocket_connection())
        if result:
            logger.info("\n✅ WebSocket infrastructure is working!")
        else:
            logger.error("\n❌ WebSocket test failed")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
