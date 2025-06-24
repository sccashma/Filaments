import sqlite3
from model.filament import Filament

class Database:
    def __init__(self, db_name='filament_data.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS filaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                color TEXT NOT NULL,
                material TEXT NOT NULL,
                weight REAL NOT NULL,
                purchase_link TEXT,
                cost REAL NOT NULL,
                RGB_color TEXT,
                k_factor REAL,
                flow_rate REAL DEFAULT 0.0
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flushing_volumes (
                from_filament_id INTEGER NOT NULL,
                to_filament_id INTEGER NOT NULL,
                volume REAL,
                PRIMARY KEY (from_filament_id, to_filament_id),
                FOREIGN KEY (from_filament_id) REFERENCES filaments(id),
                FOREIGN KEY (to_filament_id) REFERENCES filaments(id)
            )
        ''')
        self.connection.commit()

    def add_filament(self, brand, color, material, weight, purchase_link, cost, RGB_color, k_factor, flow_rate):
        self.cursor.execute('''
            INSERT INTO filaments (brand, color, material, weight, purchase_link, cost, RGB_color, k_factor, flow_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (brand, color, material, weight, purchase_link, cost, RGB_color, k_factor, flow_rate))
        self.connection.commit()

    def get_filaments(self):
        self.cursor.execute('SELECT * FROM filaments')
        return self.cursor.fetchall()

    def get_filament_by_id(self, filament_id):
        self.cursor.execute('SELECT * FROM filaments WHERE id = ?', (filament_id,))
        row = self.cursor.fetchone()
        if row:
            column_names = self.get_column_names()
            return dict(zip(column_names, row))
        return None

    def update_filament(self, filament_id, brand, color, material, weight, purchase_link, cost, RGB_color, k_factor, flow_rate):
        self.cursor.execute('''
            UPDATE filaments
            SET brand = ?, color = ?, material = ?, weight = ?, purchase_link = ?, cost = ?, RGB_color = ?, k_factor = ?, flow_rate = ?
            WHERE id = ?
        ''', (brand, color, material, weight, purchase_link, cost, RGB_color, k_factor, flow_rate, filament_id))
        self.connection.commit()

    def close(self):
        self.connection.close()

    def delete_filament(self, filament_id):
        """Delete a filament by its ID."""
        self.cursor.execute('DELETE FROM filaments WHERE id = ?', (filament_id,))
        self.connection.commit()
    
    def get_column_names(self):
        """Fetch column names from the filaments table."""
        self.cursor.execute("PRAGMA table_info(filaments)")
        return [column[1] for column in self.cursor.fetchall()]
    
    def set_flushing_volume(self, from_filament_id, to_filament_id, volume):
        """Set the flushing volume between two filaments."""
        self.cursor.execute('''
            INSERT INTO flushing_volumes (from_filament_id, to_filament_id, volume)
            VALUES (?, ?, ?)
            ON CONFLICT(from_filament_id, to_filament_id) DO UPDATE SET volume = excluded.volume
        ''', (from_filament_id, to_filament_id, volume))
        self.connection.commit()

    def get_flushing_volume(self, from_filament_id, to_filament_id):
        """Get the flushing volume between two filaments."""
        self.cursor.execute('''
            SELECT volume FROM flushing_volumes
            WHERE from_filament_id = ? AND to_filament_id = ?
        ''', (from_filament_id, to_filament_id))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_all_flushing_volumes(self):
        """Fetch all flushing volumes as a dictionary."""
        self.cursor.execute('SELECT * FROM flushing_volumes')
        return self.cursor.fetchall()