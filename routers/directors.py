import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status
from models.director import Director, DirectorCreate
from database import get_db_connection

router = APIRouter()

@router.get('/', response_model=List[Director])
def get_directors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, birthday, works FROM directors')
    directors = cursor.fetchall()
    conn.close()
    return [{
        "id": director[0],
        "name": director[1],
        "birthday": director[2],
        "works": director[3].split(', ') if director[3] else []
    } for director in directors]


@router.post('/', response_model=Director, status_code=status.HTTP_201_CREATED)
def create_director(director: DirectorCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        works_str = ', '.join(director.works)
        cursor.execute(
            "INSERT INTO directors (name, birthday, works) VALUES (?, ?, ?)",
            (director.name, director.birthday, works_str)
        )
        conn.commit()
        director_id = cursor.lastrowid
        return Director(
            id=director_id,
            name=director.name,
            birthday=director.birthday,
            works=director.works
        )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The director '{director.name}' already exists."
        )
    finally:
        conn.close()


@router.put('/{director_id}', response_model=Director)
def update_director(director_id: int, director: DirectorCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    works_str = ', '.join(director.works)
    cursor.execute(
        "UPDATE directors SET name = ?, birthday = ?, works = ? WHERE id = ?",
        (director.name, director.birthday, works_str, director_id)
    )
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail='Director not found')
    conn.commit()
    conn.close()
    return Director(
        id=director_id,
        name=director.name,
        birthday=director.birthday,
        works=director.works
    )


@router.delete('/{director_id}', response_model=dict)
def delete_director(director_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM directors WHERE id = ?", (director_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail='Director not found')
    conn.commit()
    conn.close()
    return {"detail": "Director deleted"}
