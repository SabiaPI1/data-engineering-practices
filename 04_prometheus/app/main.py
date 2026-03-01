from fastapi import FastAPI, Request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.metrics import REQUEST_COUNT, RESPONSE_TIME, CUSTOM_METRIC

app = FastAPI()

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    with RESPONSE_TIME.labels(method=method, endpoint=endpoint).time():
        response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with Prometheus!"}

@app.get("/custom")
async def custom_endpoint():
    CUSTOM_METRIC.inc()
    return {"message": "Custom metric incremented"}

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)