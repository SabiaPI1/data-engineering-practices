import requests
import time
from concurrent.futures import ThreadPoolExecutor

URL = "http://127.0.0.1:8000/data/item1"

def measure_time(url):
    start = time.time()
    response = requests.get(url)
    end = time.time()
    return response.json(), end - start

# Одиночные тесты
data, duration = measure_time(URL)
print(f"First request (from DB): {data}, Time: {duration:.4f} seconds")

data, duration = measure_time(URL)
print(f"Second request (from Cache): {data}, Time: {duration:.4f} seconds")

# Анализ производительности
def make_request():
    response = requests.get(URL)
    return response.json()

print("\nRunning load test...")
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(lambda _: make_request(), range(100)))

print(f"Completed {len(results)} concurrent requests successfully.")