import sqlite3

# Database connection
def connect_db():
    return sqlite3.connect('finance_tracker.db')

# Table for transactions (Income/Expense)
def create_transactions_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        type TEXT,  -- 'income' ya 'expense'
        category TEXT,
        amount REAL,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id))
    ''')

    conn.commit()  # Changes ko save karte hain
    conn.close()  # Connection close karte hain

# Income/Expense Add Karna
def add_transaction(user_id, type, category, amount, date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO transactions (user_id, type, category, amount, date)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, type, category, amount, date))

    conn.commit()  # Data save karte hain
    print(f"{type.capitalize()} added successfully!")  # Success message
    conn.close()  # Connection close karna

# Example Usage
create_transactions_table()  # Table banayein agar pehle se nahi bana

# Example: Income add karna
add_transaction(1, 'income', 'Salary', 5000, '2024-12-22')

# Example: Expense add karna
add_transaction(1, 'expense', 'Food', 1000, '2024-12-22')