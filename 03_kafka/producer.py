from kafka import KafkaProducer
import json
from fastapi import FastAPI

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.post("/send_event/")
def send_event(event: dict):
    try:
        producer.send('test_topic', value=event).get(timeout=10)
        return {"status": "event sent", "event": event}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("producer:app", host="127.0.0.1", port=8000, reload=True)