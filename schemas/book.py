"""
Pydantic schemas for request validation and response serialization.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ─── Review Schemas ───────────────────────────────────────────────

class ReviewCreate(BaseModel):
    """Schema for creating a new review."""
    reviewer_name: Optional[str] = Field(default="Anonymous", max_length=100)
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    content: str = Field(..., min_length=1, description="Review content")


class ReviewResponse(BaseModel):
    """Schema for review in API responses."""
    id: int
    book_id: int
    reviewer_name: str
    rating: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Book Schemas ─────────────────────────────────────────────────

class BookCreate(BaseModel):
    """Schema for creating a new book."""
    title: str = Field(..., min_length=1, max_length=255, description="Book title")
    author: str = Field(..., min_length=1, max_length=255, description="Book author")
    description: Optional[str] = Field(default=None, description="Book description")
    cover_url: Optional[str] = Field(default=None, max_length=500, description="Cover image URL")


class BookResponse(BaseModel):
    """Schema for detailed book response (includes all reviews)."""
    id: int
    title: str
    author: str
    description: Optional[str]
    cover_url: Optional[str]
    created_at: datetime
    reviews: List[ReviewResponse] = []
    review_count: int = 0
    avg_rating: float = 0.0

    class Config:
        from_attributes = True


class BookListResponse(BaseModel):
    """Schema for book in list view (summary, no full reviews)."""
    id: int
    title: str
    author: str
    description: Optional[str]
    cover_url: Optional[str]
    created_at: datetime
    review_count: int = 0
    avg_rating: float = 0.0

    class Config:
        from_attributes = True
