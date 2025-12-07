from pydantic import BaseModel
from typing import List, Optional
import datetime


class DirectorBase(BaseModel):
    director_name: str
    birthday: Optional[datetime.date]=None
    works: List[str]


class DirectorCreate(DirectorBase):
    pass


class DirectorResponse(DirectorBase):
    id: int


class Director(DirectorBase):
    id: int