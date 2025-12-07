import sqlite3

def get_db_connection():
    conn=sqlite3.connect('movies.db')
    conn.row_factory=sqlite3.Row
    return conn

def create_database():
    conn=get_db_connection()
    cursor=conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS directors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            birthday TEXT,
            works TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            director_id INTEGER,
            genres TEXT,
            average_rating REAL,
            release_year INTEGER,
            desc TEXT
            FOREIGN KEY (director_id) REFERENCES directors(id)
        )
    ''')

    conn.commit()
    return conn, cursor

def insert_directors(directors, cursor):
    director_ids={}

    for director in directors:
        cursor.execute('''
            INSERT OR IGNORE INTO director(name,birthday,works)
            VALUES (?,?,?)
        ''', (director,))
        cursor.execute('SELECT id FROM directors WHERE name=?', (director,))
        director_ids[director]=cursor.fetchone()[0]

    return director_ids

def insert_movies(movie_dict, director_ids, cursor):
    for (title,director), info in movie_dict.items():
        cursor.execute('''
            INSERT INTO movies (title, director_id, genres, average_rating, release_year, desc)
            VALUES(?,?,?,?,?,?)
        ''', (
            title,
            director_ids[director],
            ', '.join(info['genres']),
            float(info['average_rating'].split()[0]) if info['average_rating'] else None,
            int(info['release_year'].split()[0]) if info['release_year'] else None
        ))

def insert_data1(movie_dict, directors):
    conn,cursor=create_database()

    author_ids=insert_directors(directors,cursor)

    insert_movies(movie_dict, directors, cursor)

    conn.commit()
    conn.close()

