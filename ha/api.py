from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)


def get_db_connection():
    # 1. Get the path to the folder where api.py is (the 'ha' folder)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Go UP one level to the main folder, then DOWN into 'db'
    # '..' means "parent directory"
    db_path = os.path.join(current_dir, '..', 'db', 'movie_library.db')

    # 3. Resolve the path (cleans up the '..' to make it a real path)
    db_path = os.path.abspath(db_path)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/all-movies', methods=['GET'])
def get_all_movies():
    try:
        conn = get_db_connection()
        rows = conn.execute('SELECT title, poster_image,imdb_id FROM movies where watched =0 ORDER BY id DESC').fetchall()
        conn.close()

        movies_list = []
        for row in rows:
            movies_list.append({
                "title": row['title'],
                "poster": 'https://image.tmdb.org/t/p/w500'+row['poster_image'],
                "imdb_id": row['imdb_id']
            })
        return jsonify({"movies": movies_list})

    except sqlite3.OperationalError:
        return jsonify({"error": "Database not found or locked"}), 500

@app.route('/mark-watched',methods=['POST'])
def mark_movie_watched(imdb_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = 'UPDATE movies SET watched = 1 WHERE imdb_id = ?'
        cursor.execute(query, (imdb_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except sqlite3.OperationalError:
        return jsonify({"error": "Database not found or locked"}), 500




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)