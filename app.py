import time
from datetime import datetime
from flask import Flask, request
import pymongo

app = Flask(__name__)

# Устанавливаем подключение к MongoDB
client = pymongo.MongoClient('mongodb://mongohost:27017/')
db = client.counter_db  # создаем базу данных
collection = db.counter_collection  # создаем коллекцию

def get_hit_count():
    # Вставляем документ в MongoDB с датой и информацией о клиенте
    document = {
        "datetime": datetime.now().strftime('%d/%b/%Y %H:%M:%S'),
        "client_info": request.headers.get('User-Agent')
    }
    # Сохраняем запись в коллекцию
    collection.insert_one(document)
    
    # Возвращаем количество всех записей в коллекции
    return collection.count_documents({})

@app.route('/')
def hello():
    count = get_hit_count()
    return f'Hello World! I have been seen {count} times.\n'
