import unittest
from transactions import add_transaction, create_transactions_table
from budgeting import set_budget, check_budget, create_budget_table
import sqlite3

class TestFinanceTracker(unittest.TestCase):
    
    # Setup function (Test ke liye database create karna)
    def setUp(self):
        create_transactions_table()  # Transactions table banayein
        create_budget_table()  # Budget table banayein

    # Test function: Income add karna
    def test_add_income(self):
        add_transaction(1, 'income', 'Salary', 5000, '2024-12-22')
        
        # Check database for income entry
        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income' AND user_id=1")
        result = cursor.fetchone()
        conn.close()
        
        self.assertEqual(result[0], 5000)  # Ensure income is added correctly

    # Test function: Expense add karna
    def test_add_expense(self):
        add_transaction(1, 'expense', 'Food', 1000, '2024-12-22')
        
        # Check database for expense entry
        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense' AND user_id=1")
        result = cursor.fetchone()
        conn.close()

        self.assertEqual(result[0], 1000)  # Ensure expense is added correctly

    # Test function: Budget set karna
    def test_set_budget(self):
        set_budget(1, 'Food', 2000, '12', '2024')

        # Check if budget is set correctly
        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM budget WHERE user_id=1 AND category='Food' AND month='12' AND year='2024'")
        result = cursor.fetchone()
        conn.close()

        self.assertEqual(result[0], 2000)  # Ensure budget is set correctly

    # Test function: Budget exceed check karna
    def test_check_budget(self):
        set_budget(1, 'Food', 2000, '12', '2024')
        add_transaction(1, 'expense', 'Food', 2500, '2024-12-22')

        # Check if budget is exceeded
        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT SUM(amount) FROM transactions WHERE user_id = 1 AND category = 'Food' AND strftime('%m', date) = '12' AND strftime('%Y', date) = '2024'
        ''')
        total_expense = cursor.fetchone()[0] or 0
        conn.close()

        self.assertGreater(total_expense, 2000)  # Ensure expense exceeds budget

if __name__ == '_main_':
    unittest.main()