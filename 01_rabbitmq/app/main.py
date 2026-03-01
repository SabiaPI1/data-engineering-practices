from fastapi import FastAPI
from app.producer import send_message

app = FastAPI()

@app.post("/send")
def send_to_queue(message: str):
    send_message(message)
    return {"status": "Message sent", "message": message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)