from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
from etl import extract_data_from_csv, transform_data, load_data_to_db

app = FastAPI()

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        df = extract_data_from_csv(file_location)
        transformed_df = transform_data(df)
        load_data_to_db(transformed_df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при обработке файла: {str(e)}")

    return {"message": "Данные успешно загружены в SQLite"}

@app.get("/users/")
def get_users():
    import sqlite3
    conn = sqlite3.connect("etl_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    
    # Преобразуем список кортежей в список словарей для красивого JSON
    users_list = [{"id": u[0], "name": u[1], "email": u[2], "age": u[3]} for u in users]
    return {"users": users_list}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)