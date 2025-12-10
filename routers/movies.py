import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status
from models.movie import Movie, MovieCreate
from database import get_db_connection

router = APIRouter()

@router.get('/', response_model=List[Movie])
def get_movies():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, genres, average_rating, release_year, description FROM movies')
    movies = cursor.fetchall()
    conn.close()
    return [{
        "id": movie[0],
        "title": movie[1],
        "genres": movie[2].split(', ') if movie[2] else [],
        "average_rating": movie[3],
        "release_year": movie[4],
        "description": movie[5]
    } for movie in movies]


@router.post('/', response_model=Movie)
def create_movies(movie: MovieCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        genres_str = ', '.join(movie.genres)
        cursor.execute(
            "INSERT INTO movies (title, genres, average_rating, release_year, description) VALUES (?, ?, ?, ?, ?)",
            (movie.title, genres_str, movie.average_rating, movie.release_year, movie.description)
        )
        conn.commit()
        movie_id = cursor.lastrowid
        return Movie(
            id=movie_id,
            title=movie.title,
            genres=movie.genres,
            average_rating=movie.average_rating,
            release_year=movie.release_year,
            description=movie.description
        )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The movie '{movie.title}' already exists."
        )
    finally:
        conn.close()


@router.put('/{movie_id}', response_model=Movie)
def update_movies(movie_id: int, movie: MovieCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    genres_str = ', '.join(movie.genres)
    cursor.execute(
        "UPDATE movies SET title=?, genres=?, average_rating=?, release_year=?, description=? WHERE id=?",
        (movie.title, genres_str, movie.average_rating, movie.release_year, movie.description, movie_id)
    )
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail='Movie not found')
    conn.commit()
    conn.close()
    return Movie(
        id=movie_id,
        title=movie.title,
        genres=movie.genres,
        average_rating=movie.average_rating,
        release_year=movie.release_year,
        description=movie.description
    )


@router.delete('/{movie_id}', response_model=dict)
def delete_movies(movie_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id=?", (movie_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail='Movie not found')
    conn.commit()
    conn.close()
    return {"detail": "Movie deleted"}