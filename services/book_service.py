"""
Business logic layer for Book and Review operations.
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from fastapi import HTTPException, status

from models.book import Book, Review
from schemas.book import BookCreate, ReviewCreate


class BookService:
    """Service class handling all book and review business logic."""

    @staticmethod
    def get_all_books(db: Session):
        """
        Retrieve all books with their review count and average rating.
        Returns a list of book dictionaries with computed fields.
        """
        books = db.query(Book).order_by(Book.created_at.desc()).all()

        result = []
        for book in books:
            review_count = len(book.reviews)
            avg_rating = 0.0
            if review_count > 0:
                avg_rating = round(sum(r.rating for r in book.reviews) / review_count, 1)

            result.append({
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "description": book.description,
                "cover_url": book.cover_url,
                "created_at": book.created_at,
                "review_count": review_count,
                "avg_rating": avg_rating,
            })

        return result

    @staticmethod
    def get_book_by_id(db: Session, book_id: int):
        """
        Retrieve a single book by ID with all its reviews.
        Raises 404 if book not found.
        """
        book = (
            db.query(Book)
            .options(joinedload(Book.reviews))
            .filter(Book.id == book_id)
            .first()
        )

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )

        review_count = len(book.reviews)
        avg_rating = 0.0
        if review_count > 0:
            avg_rating = round(sum(r.rating for r in book.reviews) / review_count, 1)

        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "description": book.description,
            "cover_url": book.cover_url,
            "created_at": book.created_at,
            "reviews": book.reviews,
            "review_count": review_count,
            "avg_rating": avg_rating,
        }

    @staticmethod
    def create_book(db: Session, book_data: BookCreate):
        """Create a new book entry."""
        new_book = Book(
            title=book_data.title,
            author=book_data.author,
            description=book_data.description,
            cover_url=book_data.cover_url,
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)

        return {
            "id": new_book.id,
            "title": new_book.title,
            "author": new_book.author,
            "description": new_book.description,
            "cover_url": new_book.cover_url,
            "created_at": new_book.created_at,
            "reviews": [],
            "review_count": 0,
            "avg_rating": 0.0,
        }

    @staticmethod
    def create_review(db: Session, book_id: int, review_data: ReviewCreate):
        """
        Create a new review for a specific book.
        Raises 404 if book not found.
        """
        # Verify book exists
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )

        reviewer_name = review_data.reviewer_name if review_data.reviewer_name else "Anonymous"

        new_review = Review(
            book_id=book_id,
            reviewer_name=reviewer_name,
            rating=review_data.rating,
            content=review_data.content,
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        return new_review
