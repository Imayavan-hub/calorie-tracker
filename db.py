# db.py
import sqlite3

DB_NAME = "tracker.db"
import sqlite3

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        # Check if 'role' column exists, if not, add it
        c.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in c.fetchall()]
        if "role" not in columns:
            c.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
        
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

def insert_user(username, password, role="user"):
    with sqlite3.connect(DB_NAME) as conn:
        try:
            conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
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
        
def get_all_entries():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT users.username, meals.meal, meals.calories, meals.timestamp
        FROM meals
        JOIN users ON meals.user_id = users.id
        ORDER BY meals.timestamp DESC
    ''')
    data = c.fetchall()
    conn.close()
    return data

def get_user_role(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else "user"

