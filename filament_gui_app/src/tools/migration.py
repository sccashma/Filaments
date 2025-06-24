import sqlite3

def migrate_database(db_name='filament_data.db'):
    print(f"Connecting to database: {db_name}")
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Add k_factor column if it doesn't exist
    cursor.execute("PRAGMA table_info(filaments)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'k_factor' not in columns:
        cursor.execute("ALTER TABLE filaments ADD COLUMN k_factor REAL DEFAULT 0.0")
        connection.commit()

    # Add flow_rate column if it doesn't exist
    if 'flow_rate' not in columns:
        cursor.execute("ALTER TABLE filaments ADD COLUMN flow_rate REAL DEFAULT 0.0")
        connection.commit()

    connection.close()

if __name__ == "__main__":
    migrate_database()
