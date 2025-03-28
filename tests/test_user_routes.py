import pytest
from app.models import User
from app.extensions import db
from app.models.user import Role

@pytest.fixture
def sample_user():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword",
        "profile_picture":"",
        "banner":""
    }


def test_get_users(client, sample_user):
    """
    Test the GET /users endpoint to retrieve all users.
    """
    # Add a user to the database
    user = User(
        username=sample_user["username"],
        email=sample_user["email"],
        password=sample_user["password"],
        role=Role.ARTIST,
        profile_picture=sample_user["profile_picture"],
        banner=sample_user["banner"]
    )
    db.session.add(user)
    db.session.commit()

    response = client.get("/users")
    assert response.status_code == 200

    print("Retrieved Users:", response.json)

    users = response.json
    assert len(users) == 1
    assert users[0]["username"] == sample_user["username"]
    assert users[0]["email"] == sample_user["email"]


def test_get_users(client, sample_user):
    """
    Test the GET /users/<int:id> endpoint to retrieve a specific user
    """
    # Add a user to the database
    user = User(
        username=sample_user["username"],
        email=sample_user["email"],
        password=sample_user["password"],
        role=Role.ARTIST,
        profile_picture=sample_user["profile_picture"],
        banner=sample_user["banner"]
    )
    db.session.add(user)
    db.session.commit()

    response = client.get("/users/1")
    assert response.status_code == 200

    print("Retrieved User:", response.json)

    user = response.json

    assert user["username"] == sample_user["username"]
    assert user["email"] == sample_user["email"]
    assert user["profile_picture"] == sample_user["profile_picture"]
    assert user["banner"] == sample_user["banner"]
    