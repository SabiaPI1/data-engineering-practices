import redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

if __name__ == "__main__":
    redis_client.set("test_key", "Hello, Redis!")
    print(redis_client.get("test_key"))