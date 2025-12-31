import sqlite3

def create_admin():
    conn = sqlite3.connect('Ai_Engine/demodream_v2.db')
    cursor = conn.cursor()
    
    # Check if admin exists
    cursor.execute("SELECT id FROM users WHERE email='admin@demodream.com'")
    if cursor.fetchone():
        print("Admin already exists.")
    else:
        cursor.execute("INSERT INTO users (name, email, password, role, username) VALUES (?, ?, ?, ?, ?)", 
                       ("System Admin", "admin@demodream.com", "admin123", "admin", "admin"))
        conn.commit()
        print("Admin user created: admin@demodream.com / admin123")
    
    conn.close()

if __name__ == "__main__":
    create_admin()
