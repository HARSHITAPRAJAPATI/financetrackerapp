import sqlite3

# Database connection function
def connect_db():
    return sqlite3.connect('finance_tracker.db')

# Budget Table Create Karna (agar pehle se nahi hai)
def create_budget_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        category TEXT,
        amount REAL,
        month TEXT,
        year TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id))
    ''')

    conn.commit()
    conn.close()

# Budget Set Karna (User ke liye)
def set_budget(user_id, category, amount, month, year):
    conn = connect_db()
    cursor = conn.cursor()

    # Check karna ki budget pehle se exist to nahi karta
    cursor.execute('''
    SELECT * FROM budget 
    WHERE user_id = ? AND category = ? AND month = ? AND year = ?
    ''', (user_id, category, month, year))

    if cursor.fetchone():
        print("Budget already set for this category in this month!")
    else:
        # Budget set karna
        cursor.execute('''
        INSERT INTO budget (user_id, category, amount, month, year)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, category, amount, month, year))

        conn.commit()
        print(f"Budget for {category} in {month}/{year} set to {amount}")
    
    conn.close()

# Budget Check Karna (Exceed hua hai ya nahi)
def check_budget(user_id, category, month, year):
    conn = connect_db()
    cursor = conn.cursor()

    # User ka budget fetch karna
    cursor.execute('''
    SELECT amount FROM budget 
    WHERE user_id = ? AND category = ? AND month = ? AND year = ?
    ''', (user_id, category, month, year))
    
    budget = cursor.fetchone()
    if budget:
        budget_amount = budget[0]
        
        # User ka total expense fetch karna for this category
        cursor.execute('''
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND type = 'expense' AND category = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
        ''', (user_id, category, month, year))

        total_expense = cursor.fetchone()[0] or 0  # Agar expense nahi hai toh 0 consider karna
        
        print(f"Total Expense for {category} in {month}/{year}: {total_expense}")
        
        # Budget exceed check karna
        if total_expense > budget_amount:
            print(f"Warning: You have exceeded your budget for {category}!")
        else:
            print(f"You are within your budget for {category}.")
    else:
        print(f"No budget set for {category} in {month}/{year}.")
    
    conn.close()

# Example Usage
create_budget_table()  # Budget table banayein agar nahi bana

# Example: Budget set karna
set_budget(1, 'Food', 2000, '12', '2024')  # December 2024 ke liye Food category ka budget

# Example: Budget check karna
check_budget(1, 'Food', '12', '2024')  # December 2024 ke liye Food category ka budget check karna