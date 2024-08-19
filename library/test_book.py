# Watthana Siamliem 653380280-0

import pytest
from main import Book

def test_add_book(db_session):
    # Create a new book instance
    new_book = Book(title="Test Book", firstauthor="Test Author", isbn="1234567890")
    db_session.add(new_book)
    db_session.commit()

    # Query the book to see if it is there
    book = db_session.query(Book).filter_by(isbn="1234567890").first()
    assert book is not None
    assert book.title == "Test Book"

def test_delete_book(db_session):
    # Add a book, then remove this new book from the db
    book = Book(title="Test Book 2", firstauthor="Test Author 2", isbn="0987654321")
    db_session.add(book)
    db_session.commit()

    # Delete the book
    db_session.delete(book)
    db_session.commit()

    # Query the book to check if it is removed from the db
    deleted_book = db_session.query(Book).filter_by(isbn="0987654321").first()
    assert deleted_book is None
