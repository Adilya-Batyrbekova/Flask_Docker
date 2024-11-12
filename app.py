import time
import redis
import psycopg2
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)
cache = redis.Redis(host='redishost', port=6379)

# Подключение к PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host='postgresqlhost',
        database='counterdb',
        user='postgres',
        password='password'
    )
    return conn

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    
    # Сохранение информации о запросе в PostgreSQL
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO requests (datetime, client_info)
        VALUES (%s, %s)
    ''', (datetime.now(), request.headers.get('User-Agent')))
    conn.commit()
    cur.close()
    conn.close()
    
    return f'Hello World! I have been seen {count} times.\n'
