import sqlite3
import shutil
import os

# Database connection function
def connect_db():
    return sqlite3.connect('finance_tracker.db')

# Backup Function: Database ka backup banayein
def backup_data():
    try:
        # Backup file ka naam
        backup_filename = 'finance_tracker_backup.db'
        
        # Agar backup file already exist karti ho, toh usse remove kar dein
        if os.path.exists(backup_filename):
            os.remove(backup_filename)
        
        # Original database file ka path
        original_db = 'finance_tracker.db'
        
        # Backup banane ke liye shutil ka use karenge
        shutil.copy(original_db, backup_filename)
        print(f"Database backup successful! Backup saved as {backup_filename}")
    except Exception as e:
        print(f"Error during backup: {e}")

# Restore Function: Backup se database restore karna
def restore_data():
    try:
        # Backup file ka naam
        backup_filename = 'finance_tracker_backup.db'
        
        # Agar backup file exist nahi karti, toh error
        if not os.path.exists(backup_filename):
            print("No backup file found to restore.")
            return
        
        # Original database ko overwrite karenge backup se
        shutil.copy(backup_filename, 'finance_tracker.db')
        print("Database restored successfully from backup.")
    except Exception as e:
        print(f"Error during restore: {e}")

# Example Usage
backup_data()  # Backup create karna
# restore_data()  # Agar restore karna ho, toh is line ko uncomment karke run kar sakte hain