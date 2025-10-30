from enum import Enum
from pydantic import BaseModel
from typing import Optional


class ReviewStatus(str, Enum):
    watching = "watching"
    completed = "completed"
    planned = "planned"
    dropped = "dropped"
    paused = "paused"
    not_specified = "not_specified"


class ReviewCreateClass(BaseModel):
    anime_id: int
    status: Optional[ReviewStatus] = ReviewStatus.not_specified
    rating: Optional[int] = None
    review_text: Optional[str] = None


class ReviewInputClass(ReviewCreateClass):
    user_id: int
