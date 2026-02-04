import sqlite3

def save_movie_to_db(imdb_id,title):
    conn = sqlite3.connect('../movie_library.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT OR IGNORE INTO movies(imdb_id,title) values (?,?)''',(imdb_id,title))
    conn.commit()
    conn.close()
