import sqlite3

# Database connection
def connect_db():
    return sqlite3.connect('finance_tracker.db')

# Database setup - Users table create karna
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT)
    ''')

    conn.commit()  # Changes ko save karte hain
    conn.close()  # Connection close karte hain

# User Registration - User ko register karna
def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()  # Data save karna
        print("Registration successful!")  # Success message
    except sqlite3.IntegrityError:
        print("Username already exists.")  # Agar username pehle se ho toh
    conn.close()  # Connection close karna

# User Login - User ko login karna
def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()  # Agar user milta hai toh

    if user:
        print("Login successful!")  # Agar login successful ho
    else:
        print("Invalid username or password.")  # Agar username ya password galat ho
    conn.close()  # Connection close karna

# Table banayein agar pehle se nahi bana
create_table()

# Example Usage
register_user('harshi', 'password123')  # Registration ke liye example
login_user('harshi', 'password123')  # Login ke liye example