# Flask_Docker

### 1. Подготовка файлов для проекта:
Обновим app.py.
Настроим Dockerfile и docker-compose.yml, добавив сервисы для MongoDB.
### 2. Изменение кода приложения app.py:
Для хранения данных в базе данных вам нужно будет добавить зависимости, подключить Flask к базе данных, сохранить информацию о каждом запросе и включить в вывод количество запросов и время
Изменённый app.py с MongoDB
```
import time
from flask import Flask, request
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)

# Подключение к MongoDB
client = MongoClient("mongodb://mongohost:27017/")
db = client["flaskdb"]
collection = db["requests"]

@app.route('/')
def hello():
    # Счетчик запросов
    count = collection.count_documents({})
    count += 1

    # Данные о клиенте и времени
    request_data = {
        "count": count,
        "datetime": datetime.now().strftime("%d/%b/%Y %H:%M:%S"),
        "client_info": request.headers.get("User-Agent")
    }
    
    # Сохранение данных запроса
    collection.insert_one(request_data)
    
    return 'Hello World! I have been seen {} times.\n'.format(count)
```