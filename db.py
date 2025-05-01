# db.py
import sqlite3

DB_NAME = "tracker.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS meals (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        meal TEXT,
                        calories REAL,
                        ingredients TEXT,
                        date TEXT,
                        timestamp TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
        conn.commit()

def insert_user(username, password):
    with sqlite3.connect(DB_NAME) as conn:
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def validate_user(username, password):
    with sqlite3.connect(DB_NAME) as conn:
        user = conn.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        return user[0] if user else None

def insert_meal(user_id, meal, calories, ingredients, date, timestamp):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''INSERT INTO meals (user_id, meal, calories, ingredients, date, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?)''', (user_id, meal, calories, ingredients, date, timestamp))
        conn.commit()

def get_meals(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT * FROM meals WHERE user_id=?", (user_id,)).fetchall()

def get_meals_by_date(user_id, date):
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT * FROM meals WHERE user_id=? AND date=?", (user_id, date)).fetchall()

def get_summary(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT date, SUM(calories) FROM meals WHERE user_id=? GROUP BY date", (user_id,)).fetchall()

def get_total_calories(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        row = conn.execute("SELECT SUM(calories) FROM meals WHERE user_id=?", (user_id,)).fetchone()
        return row[0] if row[0] else 0
