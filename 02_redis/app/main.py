from fastapi import FastAPI, HTTPException
from app.redis_utils import redis_client
from app.database import get_data_from_db

app = FastAPI()

@app.get("/")
async def root():
    redis_client.set("greeting", "Hello, Redis!")
    greeting = redis_client.get("greeting")
    return {"message": greeting}

@app.get("/data/{key}")
async def get_data(key: str):
    try:
        # Шаг 1: Попытка получить данные из кеша
        cached_data = redis_client.get(key)
        if cached_data:
            return {"source": "cache", "data": cached_data}

        # Шаг 2: Запрос к БД
        db_data = get_data_from_db(key)
        if db_data:
            # Сохранение в кеш с TTL 5 минут (300 сек)
            redis_client.setex(key, 300, db_data)
            return {"source": "database", "data": db_data}

        raise HTTPException(status_code=404, detail="Data not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)