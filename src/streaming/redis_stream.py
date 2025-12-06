"""
Real-time data streaming with Redis
"""
import json
import asyncio
from datetime import datetime
from loguru import logger

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not installed. Install with: pip install redis")

class RedisStreamer:
    """Redis-based real-time data streaming"""
    
    def __init__(self, host='localhost', port=6379):
        if not REDIS_AVAILABLE:
            logger.warning("Redis client not available")
            self.redis_client = None
            return
        
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                decode_responses=True,
                socket_connect_timeout=2
            )
            # Test connection
            self.redis_client.ping()
            logger.info(f"✅ Redis connected: {host}:{port}")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            self.redis_client = None
    
    def publish_volatility(self, pair, data):
        """Publish volatility data to Redis stream"""
        if not self.redis_client:
            return False
        
        try:
            # Add to stream
            stream_key = f"volatility:{pair}"
            message = {
                'timestamp': datetime.now().isoformat(),
                'price': str(data.get('price', 0)),
                'realized_vol': str(data.get('realized_vol', 0)),
                'implied_vol': str(data.get('implied_vol', 0)),
                'garch_forecast': str(data.get('garch_forecast', 0)),
                'spread': str(data.get('spread', 0))
            }
            
            # Add to stream with max length to prevent unlimited growth
            self.redis_client.xadd(
                stream_key,
                message,
                maxlen=1000,  # Keep last 1000 entries
                approximate=True
            )
            
            # Also publish to pub/sub for instant notifications
            channel = f"volatility_updates:{pair}"
            self.redis_client.publish(channel, json.dumps(data))
            
            # Cache latest value
            cache_key = f"latest:{pair}"
            self.redis_client.setex(
                cache_key,
                3600,  # 1 hour TTL
                json.dumps(data)
            )
            
            logger.debug(f"Published {pair} to Redis")
            return True
            
        except Exception as e:
            logger.error(f"Redis publish failed: {e}")
            return False
    
    def get_latest(self, pair):
        """Get latest volatility from cache"""
        if not self.redis_client:
            return None
        
        try:
            cache_key = f"latest:{pair}"
            data = self.redis_client.get(cache_key)
            
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Redis get failed: {e}")
            return None
    
    def get_stream(self, pair, count=10):
        """Get recent entries from stream"""
        if not self.redis_client:
            return []
        
        try:
            stream_key = f"volatility:{pair}"
            
            entries = self.redis_client.xrevrange(stream_key, count=count)
            
            results = []
            for entry_id, fields in entries:
                results.append({
                    'id': entry_id,
                    'timestamp': fields['timestamp'],
                    'price': float(fields['price']),
                    'realized_vol': float(fields['realized_vol']),
                    'implied_vol': float(fields['implied_vol']),
                    'garch_forecast': float(fields['garch_forecast']),
                    'spread': float(fields['spread'])
                })
            
            return results
        except Exception as e:
            logger.error(f"Redis get_stream failed: {e}")
            return []
    
    async def subscribe(self, pair, callback):
        """Subscribe to real-time updates"""
        if not self.redis_client:
            logger.warning("Redis not available for subscription")
            return
        
        try:
            pubsub = self.redis_client.pubsub()
            channel = f"volatility_updates:{pair}"
            pubsub.subscribe(channel)
            
            logger.info(f"Subscribed to {channel}")
            
            for message in pubsub.listen():
                if message['type'] == 'message':
                    data = json.loads(message['data'])
                    await callback(data)
        except Exception as e:
            logger.error(f"Redis subscription failed: {e}")
    
    def get_all_pairs(self):
        """Get list of all pairs with data"""
        if not self.redis_client:
            return []
        
        try:
            keys = self.redis_client.keys("latest:*")
            return [key.replace("latest:", "") for key in keys]
        except Exception as e:
            logger.error(f"Redis get_all_pairs failed: {e}")
            return []

class KafkaStreamer:
    """Kafka-based high-throughput streaming"""
    
    def __init__(self, bootstrap_servers='localhost:9092'):
        try:
            from kafka import KafkaProducer
            
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                request_timeout_ms=5000,
                max_block_ms=5000
            )
            
            logger.info(f"✅ Kafka producer connected: {bootstrap_servers}")
            self.available = True
            
        except ImportError:
            logger.warning("Kafka not installed. Install with: pip install kafka-python")
            self.producer = None
            self.available = False
        except Exception as e:
            logger.warning(f"Kafka connection failed: {e}")
            self.producer = None
            self.available = False
    
    def publish_volatility(self, pair, data):
        """Publish to Kafka topic"""
        if not self.available or not self.producer:
            return False
        
        try:
            topic = f"volatility.{pair.replace('/', '.')}"
            
            self.producer.send(topic, {
                'timestamp': datetime.now().isoformat(),
                'pair': pair,
                **data
            })
            
            self.producer.flush()
            
            logger.debug(f"Published {pair} to Kafka")
            return True
            
        except Exception as e:
            logger.error(f"Kafka publish failed: {e}")
            return False
    
    def consume(self, pair, callback):
        """Consume from Kafka topic"""
        if not self.available:
            logger.warning("Kafka not available")
            return
        
        try:
            from kafka import KafkaConsumer
            
            topic = f"volatility.{pair.replace('/', '.')}"
            
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers='localhost:9092',
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest'
            )
            
            logger.info(f"Consuming from {topic}")
            
            for message in consumer:
                callback(message.value)
                
        except Exception as e:
            logger.error(f"Kafka consume failed: {e}")

# Integration with AgentSpoons
class StreamingIntegration:
    """Integrate streaming into AgentSpoons"""
    
    def __init__(self, use_redis=True, use_kafka=False):
        self.redis = None
        self.kafka = None
        
        if use_redis:
            try:
                self.redis = RedisStreamer()
            except Exception as e:
                logger.warning(f"Failed to initialize Redis: {e}")
        
        if use_kafka:
            try:
                self.kafka = KafkaStreamer()
            except Exception as e:
                logger.warning(f"Failed to initialize Kafka: {e}")
        
        if not self.redis and not self.kafka:
            logger.warning("No streaming backends available")
    
    def publish_update(self, pair, data):
        """Publish to all configured streams"""
        success = False
        
        if self.redis:
            success = self.redis.publish_volatility(pair, data) or success
        
        if self.kafka:
            success = self.kafka.publish_volatility(pair, data) or success
        
        return success
    
    def get_latest(self, pair):
        """Get latest data (prefer Redis cache)"""
        if self.redis:
            return self.redis.get_latest(pair)
        return None
    
    def get_stream(self, pair, count=10):
        """Get historical stream data"""
        if self.redis:
            return self.redis.get_stream(pair, count)
        return []
    
    def get_all_pairs(self):
        """Get all pairs with streaming data"""
        if self.redis:
            return self.redis.get_all_pairs()
        return []
    
    def is_available(self):
        """Check if any streaming backend is available"""
        return bool(self.redis or self.kafka)

# Global streaming instance
streaming = StreamingIntegration(use_redis=True, use_kafka=False)
