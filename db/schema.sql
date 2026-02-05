DROP TABLE IF EXISTS movies;

CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imdb_id TEXT UNIQUE,
    title TEXT,
	poster_image TEXT,
    watched INTEGER DEFAULT 0
);