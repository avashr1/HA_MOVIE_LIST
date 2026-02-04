import sqlite3
import os


def init_database():
    # Since we are running INSIDE the folder, we just use the filenames
    db_file = 'movie_library.db'
    schema_file = 'schema.sql'

    # Check if schema file exists before trying to read it
    if not os.path.exists(schema_file):
        print(f"Error: Could not find '{schema_file}' in the current folder.")
        return

    # Connect (This creates the file if it's missing)
    conn = sqlite3.connect(db_file)

    print(f"Connected to {db_file}...")

    try:
        with open(schema_file, 'r') as f:
            # executescript can run multiple SQL commands (Drop + Create) at once
            conn.executescript(f.read())
        print("Success! Table dropped and recreated.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


if __name__ == '__main__':
    init_database()