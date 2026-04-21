"""
Book Review Hub — FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from controllers.book_controller import router as book_router

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Book Review Hub API",
    description="API for managing books and reviews",
    version="1.0.0",
)

# CORS configuration — allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(book_router)


@app.get("/", tags=["Root"])
def root():
    """Health check endpoint."""
    return {"message": "Book Review Hub API is running!", "docs": "/docs"}
