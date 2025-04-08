import sqlite3

DB_NAME = "quizbowl.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    subjects = ['Intro to Project Management', 
                'Database Management',
                'Supply Chain Management', 
                'Data Driven Decision Making',
                'Business Applications Devlopment']
    for subject in subjects:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {subject} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer TEXT NOT NULL
            )
        ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized with subject tables.")
