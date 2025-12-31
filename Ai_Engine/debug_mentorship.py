import sqlite3
import json

def test_query():
    conn = sqlite3.connect('Ai_Engine/demodream_v2.db')
    cursor = conn.cursor()
    
    # Check Guide Profile for user wer@gmail.com (ID 5)
    cursor.execute("SELECT id FROM users WHERE email='wer@gmail.com'")
    user_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT expertise_fields FROM guide_profiles WHERE user_id=?", (user_id,))
    expertise_str = cursor.fetchone()[0]
    expertise = json.loads(expertise_str)
    print(f"Expertise for user {user_id}: {expertise}")
    
    # Mock the SQLAlchemy query logic
    cursor.execute("SELECT id, field, status FROM mentorship_requests")
    reqs = cursor.fetchall()
    results = []
    for r_id, field, status in reqs:
        if field in expertise and status == "open":
            results.append(r_id)
            
    print(f"Matching Request IDs: {results}")
    conn.close()

if __name__ == "__main__":
    test_query()
