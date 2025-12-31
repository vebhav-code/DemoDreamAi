import sqlite3

def add_column():
    try:
        conn = sqlite3.connect('demodream_v2.db')
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT")
        conn.commit()
        print("Column 'role' added successfully.")
    except sqlite3.OperationalError as e:
        print(f"Operation failed (column might already exist): {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_column()
