import pytest
from app.models import User
from app.extensions import db

@pytest.fixture
def sample_user():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword",
        "profile_picture": "/static/default_profile.png",
        "banner": "/static/default_banner.png"
    }

def test_add_user(client, sample_user):
    """
    Test the POST /users endpoint to add a new user.
    """
    response = client.post("/users", json=sample_user)
    assert response.status_code == 201
    assert response.json["message"] == "User created successfully"

    # Verify the user was added to the database
    user = User.query.filter_by(username="testuser").first()
    assert user is not None
    assert user.email == "testuser@example.com"


def test_get_users(client, sample_user):
    """
    Test the GET /users endpoint to retrieve all users.
    """
    # Add a user to the database
    user = User(
        username=sample_user["username"],
        email=sample_user["email"],
        password=sample_user["password"],
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
    assert users[0]["username"] == "testuser"
    assert users[0]["email"] == "testuser@example.com"