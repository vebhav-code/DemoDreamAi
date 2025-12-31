import sqlite3

def fix_domains():
    conn = sqlite3.connect('Ai_Engine/demodream_v2.db')
    cursor = conn.cursor()
    
    mapping = {
        'software_engineering': 'Software Engineering',
        'data_science': 'Data Science',
        'product_management': 'Product Management',
        'ui_ux_design': 'UI/UX Design',
        'marketing': 'Marketing',
        'finance': 'Finance'
    }
    
    for old, new in mapping.items():
        cursor.execute("UPDATE guides SET primary_domain=? WHERE primary_domain=?", (new, old))
        cursor.execute("UPDATE guide_profiles SET expertise_fields = REPLACE(expertise_fields, ?, ?)", (f'"{old}"', f'"{new}"'))
        # Specific check for Software Dev which was in GuideProfile
        cursor.execute("UPDATE guide_profiles SET expertise_fields = REPLACE(expertise_fields, '\"Software Dev\"', '\"Software Engineering\"')")
    
    conn.commit()
    print("Database sync complete.")
    conn.close()

if __name__ == "__main__": fix_domains()
