import sqlite3

def create_user(name, email, password):
    try:
        conn = sqlite3.connect('Ai_Engine/demodream_v2.db')
        cursor = conn.cursor()
        # Default role explorer as per logic
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, 'explorer')", (name, email, password))
        conn.commit()
        print("SUCCESS")
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    create_user("Harsh", "harsh@gmail.com", "123123")
