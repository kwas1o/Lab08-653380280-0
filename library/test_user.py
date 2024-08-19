# Watthana Siamliem 653380280-0

import pytest
from main import User

def test_add_user(db_session):
    # Create a new user instance
    new_user = User(username="test_newuser1", fullname="Test User 1")
    db_session.add(new_user)
    db_session.commit()

    # Query the test_newuser1 to see if it is there
    user = db_session.query(User).filter_by(username="test_newuser1").first()
    assert user is not None
    assert user.username == "test_newuser1"

def test_delete_user(db_session):
    # Add a user, then remove this new user from the db
    user = User(username="test_newuser2", fullname="Test User 2")
    db_session.add(user)
    db_session.commit()

    # Delete the test_newuser2
    db_session.delete(user)
    db_session.commit()

    # Query the test_newuser2 to check if it is removed from the db
    deleted_user = db_session.query(User).filter_by(username="test_newuser2").first()
    assert deleted_user is None
