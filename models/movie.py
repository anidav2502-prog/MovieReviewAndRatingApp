from pydantic import BaseModel
from typing import List, Optional

class MovieBase(BaseModel):
    title: str
    director_id: int
    genres: List[str]
    average_rating: Optional[float] = None
    release_year: Optional[int] = None
    description: str

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int

class Movie(MovieBase):
    id: int