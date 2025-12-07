from pydantic import BaseModel
from typing import List, Optional

class ReviewBase(BaseModel):
    review_text: Optional[str]=None
    movie_id: int
    rating: float

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int

class Review(ReviewBase):
    id: int