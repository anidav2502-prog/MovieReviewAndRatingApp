import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status
from models.review import Review, ReviewCreate
from database import get_db_connection

router = APIRouter()

@router.get('/', response_model=List[Review])
def get_reviews():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, review_text, rating FROM reviews')
    reviews = cursor.fetchall()
    conn.close()
    return [{
        "id": review[0],
        "review_text": review[1],
        "rating": review[2]
    } for review in reviews]


@router.post('/', response_model=Review)
def create_reviews(review: ReviewCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO reviews (review_text, rating) VALUES (?, ?)",
            (review.review_text, review.rating)
        )
        conn.commit()
        review_id = cursor.lastrowid
        return Review(
            id=review_id,
            review_text=review.review_text,
            rating=review.rating,
        )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
        )
    finally:
        conn.close()


@router.put('/{review_id}', response_model=Review)
def update_reviews(review_id: int, review: ReviewCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE reviews SET review_text=?, rating=? WHERE id=?",
        (review.review_text, review.rating,review_id)
    )
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail='Review not found')
    conn.commit()
    conn.close()
    return Review(
        id=review_id,
        review_text=review.review_text,
        rating=review.rating
    )


@router.delete('/{review_id}', response_model=dict)
def delete_reviews(review_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reviews WHERE id=?", (review_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail='Review not found')
    conn.commit()
    conn.close()
    return {"detail": "Review deleted"}
