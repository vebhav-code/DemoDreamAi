import sqlite3

def verify_all_guides():
    try:
        conn = sqlite3.connect('Ai_Engine/demodream_v2.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE guides SET verified = 1")
        conn.commit()
        count = cursor.rowcount
        print(f"Verified {count} guides.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    verify_all_guides()
