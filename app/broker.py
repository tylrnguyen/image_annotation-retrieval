import redis 
import json
import threading

class Broker: 
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def publish(self, channel, message):
        self.redis_client.publish(channel, json.dumps(message))

    def subscribe(self, channel, callback):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)

        def listen():
            try:
                for message in pubsub.listen():
                    if message["type"] == "message":
                        data = json.loads(message["data"])
                        callback(data)
            except (redis.exceptions.ConnectionError, ValueError):
                pass


        thread = threading.Thread(target=listen, daemon=True)
        thread.start()

        return pubsub