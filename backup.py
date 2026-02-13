import shutil
import os
from datetime import datetime

def backup_database():
    source = 'portfolio.db'
    backup_dir = 'backups'
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Created directory: {backup_dir}")

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = os.path.join(backup_dir, f"portfolio_backup_{timestamp}.db")

    try:
        if os.path.exists(source):
            shutil.copy2(source, destination)
            print(f"Backup successful: {destination}")
        else:
            print("Error: portfolio.db not found. Run app.py first.")
    except Exception as e:
        print(f"Backup failed: {e}")

if __name__ == "__main__":
    backup_database()