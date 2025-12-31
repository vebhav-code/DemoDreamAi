import sqlite3
import sys

def check_user(email):
    try:
        conn = sqlite3.connect('Ai_Engine/demodream_v2.db')
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        if result:
            print("EXISTS")
        else:
            print("NOT EXISTS")
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    check_user("harsh@gmail.com")
