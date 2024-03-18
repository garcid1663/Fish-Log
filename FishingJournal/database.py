# database.py
import sqlite3

def create_connection():
    """Create a database connection and return the connection object."""
    conn = None
    try:
        conn = sqlite3.connect('my_data.db')
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")  # This line will print the exact error
    return conn

#ADDED PRIMARY KEY AUTO
def create_table():
    """Create the table with four columns."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    column1 TEXT, 
                    column2 TEXT,
                    column3 TEXT,
                    column4 TEXT,
                    column5 TEXT
                )
            ''')
            conn.commit()
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")

def insert_entry(column1, column2, column3, column4, column5):
    """Insert a new entry into the entries table."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO entries (column1, column2, column3, column4, column5) VALUES (?, ?, ?, ?, ?)', 
                           (column1, column2, column3, column4, column5))
            conn.commit()
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")

def search_database(query):
    """Search for the given query in the database and return the results."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Use a wildcard search for a match in any of the columns
            cursor.execute("SELECT * FROM entries WHERE column1 LIKE ? OR column2 LIKE ? OR column3 LIKE ? OR column4 LIKE ? OR column5 LIKE ?", 
                           ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
            return cursor.fetchall()
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")
        return []
    
def get_total_lbs_caught():
    """Return the total weight of all fish caught."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(column2) FROM entries")
            total = cursor.fetchone()[0]
            return total if total else 0
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")
        return 0
    
def delete_entry(entry_id):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            print(f"Deleting entry with ID: {entry_id}")
            # The id needs to be passed as a tuple
            cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
            conn.commit()
            print("Deletion committed.")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")




