# Watthana Siamliem 653380280-0

import pytest
from fastapi.testclient import TestClient
from main import app, get_db, User, Book, Borrowlist

# Create a test client to interact with the API
@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.mark.parametrize("username, fullname", [("test_user1", "Test User 1"), ("test_user2", "Test User 2")])
def test_create_user(client, db_session, username, fullname):
    response = client.post(f"/users/?username={username}&fullname={fullname}")
    assert response.status_code == 200
    assert response.json()["username"] == username
    assert response.json()["fullname"] == fullname
    assert db_session.query(User).filter_by(username=username).first()

@pytest.mark.parametrize("title, firstauthor, isbn", [("Test Book 1", "Test Author 1", "1234567890"), ("Test Book 2", "Test Author 2", "0987654321")])
def test_create_book(client, db_session, title, firstauthor, isbn):
    response = client.post(f"/books/?title={title}&firstauthor={firstauthor}&isbn={isbn}")
    assert response.status_code == 200
    assert response.json()["title"] == title
    assert response.json()["firstauthor"] == firstauthor
    assert response.json()["isbn"] == isbn
    assert db_session.query(Book).filter_by(isbn=isbn).first()

def test_create_borrowlist(client, db_session):
    new_user = User(username="testuser", fullname="Test User")
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    new_book = Book(title="Test Book", firstauthor="Test Author", isbn="1234567890")
    db_session.add(new_book)
    db_session.commit()
    db_session.refresh(new_book)

    response = client.post(f"/borrowlist/?user_id={new_user.id}&book_id={new_book.id}")
    assert response.status_code == 200
    borrowlist_entry = db_session.query(Borrowlist).filter_by(user_id=new_user.id, book_id=new_book.id).first()
    assert borrowlist_entry is not None
    assert borrowlist_entry.user_id == new_user.id
    assert borrowlist_entry.book_id == new_book.id

def test_get_borrowed_books(client, db_session):
    # Create a new user
    new_user = User(username="testuser2", fullname="Test User 2")
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    # Create a new book
    new_book = Book(title="Another Test Book", firstauthor="Another Test Author", isbn="0987654321")
    db_session.add(new_book)
    db_session.commit()
    db_session.refresh(new_book)

    # Create a borrow list entry
    borrowlist_entry = Borrowlist(user_id=new_user.id, book_id=new_book.id)
    db_session.add(borrowlist_entry)
    db_session.commit()

    # Makes a GET request to the /borrowlist/{user_id} endpoint
    response = client.get(f"/borrowlist/{new_user.id}")

    # Checks that the API request was successful
    assert response.status_code == 200

    # Checks that the borrowed books returned by the API match what we expect
    borrowed_books = response.json()
    assert len(borrowed_books) == 1
    assert borrowed_books[0]["book_id"] == new_book.id
