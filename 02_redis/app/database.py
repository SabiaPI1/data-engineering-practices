FAKE_DB = {
    "item1": "Value 1",
    "item2": "Value 2",
    "item3": "Value 3",
}

def get_data_from_db(key: str):
    return FAKE_DB.get(key)