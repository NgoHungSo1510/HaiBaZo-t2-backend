"""
API route handlers (Controller layer) for Book and Review endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.book import (
    BookCreate,
    BookResponse,
    BookListResponse,
    ReviewCreate,
    ReviewResponse,
)
from services.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookListResponse])
def list_books(db: Session = Depends(get_db)):
    """Get all books with summary info (review count, avg rating)."""
    return BookService.get_all_books(db)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific book, including all reviews."""
    return BookService.get_book_by_id(db, book_id)


@router.post("/", response_model=BookResponse, status_code=201)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """Create a new book entry."""
    return BookService.create_book(db, book_data)


@router.post("/{book_id}/reviews", response_model=ReviewResponse, status_code=201)
def create_review(book_id: int, review_data: ReviewCreate, db: Session = Depends(get_db)):
    """Create a new review for a specific book."""
    return BookService.create_review(db, book_id, review_data)
