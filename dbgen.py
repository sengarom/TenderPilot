import sqlite3
import os

def initialize_db():
    db_folder = 'db'
    db_path = os.path.join(db_folder, 'items.db')
    os.makedirs(db_folder, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items_master (
            item_name TEXT,
            description TEXT,
            cost_price REAL
        )
    ''')
    sample_items = [
        ('Security Camera', 'HD night vision security camera', 120.0),
        ('Motion Detector', 'Infrared motion sensor for indoor/outdoor use', 45.5),
        ('Alarm Panel', 'Touchscreen alarm control panel', 200.0),
        ('Door Sensor', 'Wireless door/window entry sensor', 18.75),
        ('Floodlight', 'Outdoor security floodlight with motion activation', 65.0)
    ]
    cursor.executemany('INSERT INTO items_master (item_name, description, cost_price) VALUES (?, ?, ?)', sample_items)
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path} with sample data.")

if __name__ == "__main__":
    initialize_db()
