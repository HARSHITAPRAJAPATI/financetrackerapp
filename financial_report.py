import sqlite3

# Database connection function
def connect_db():
    return sqlite3.connect('finance_tracker.db')

# Monthly aur Yearly Reports Generate Karna
def generate_reports(user_id, year, month=None):
    conn = connect_db()
    cursor = conn.cursor()

    # Monthly Report (Agar month diya gaya ho)
    if month:
        cursor.execute('''
        SELECT type, SUM(amount) 
        FROM transactions 
        WHERE user_id = ? AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
        GROUP BY type
        ''', (user_id, year, month))
    # Yearly Report (Agar month nahi diya gaya ho)
    else:
        cursor.execute('''
        SELECT type, SUM(amount) 
        FROM transactions 
        WHERE user_id = ? AND strftime('%Y', date) = ?
        GROUP BY type
        ''', (user_id, year))

    result = cursor.fetchall()

    # Results ko print karna
    income = 0
    expense = 0
    for row in result:
        if row[0] == 'income':
            income = row[1]
        elif row[0] == 'expense':
            expense = row[1]

    savings = income - expense  # Savings = Income - Expense

    # Report Print Karna
    print(f"Report for {year}")
    if month:
        print(f"Month: {month}")
    print(f"Total Income: {income}")
    print(f"Total Expense: {expense}")
    print(f"Total Savings: {savings}")

    conn.close()

# Example Usage
generate_reports(1, '2024', '12')  # Monthly report for December 2024
generate_reports(1, '2024')  # Yearly report for 2024