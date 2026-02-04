import os
import sqlite3

def save_movie_to_db(imdb_id,title,poster_image):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'db', 'movie_library.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''INSERT OR IGNORE INTO movies(imdb_id,title,poster_image) values (?,?,?)''',(imdb_id,title,poster_image))
    conn.commit()
    conn.close()
