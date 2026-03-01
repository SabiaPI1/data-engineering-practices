import sqlite3
import pandas as pd

DB_PATH = "etl_data.db"

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            age INTEGER
        )
    """)
    conn.commit()
    conn.close()

def extract_data_from_csv(csv_file: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(csv_file, encoding="utf-8-sig", sep=";")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        raise ValueError(f"Ошибка чтения CSV: {str(e)}")

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    expected_columns = {"name", "email", "age"}
    if not expected_columns.issubset(set(df.columns)):
        raise ValueError(f"Ожидаемые колонки: {expected_columns}, но получили: {set(df.columns)}")

    df = df.dropna()
    df["name"] = df["name"].astype(str).str.title().str.strip()
    df["email"] = df["email"].astype(str).str.lower().str.strip()
    
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df = df.dropna(subset=["age"])
    df["age"] = df["age"].astype(int)
    
    # Оставляем только совершеннолетних
    df = df[df["age"] > 18]
    return df

def load_data_to_db(df: pd.DataFrame):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        try:
            cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                           (row["name"], row["email"], row["age"]))
        except sqlite3.IntegrityError:
            pass # Игнорируем дубликаты email

    conn.commit()
    conn.close()

setup_database()