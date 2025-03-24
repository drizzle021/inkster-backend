import pytest
from app.models import User
from app.extensions import db

@pytest.fixture
def sample_user():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword",
        "profile_picture":"",
        "banner":""
    }

def test_add_user(client, sample_user):
    """
    Test the POST /auth/register endpoint to add a new user.
    """
    response = client.post("/auth/register", json=sample_user)
    assert response.status_code == 201
    assert response.json["message"] == "New user added successfully"

    # Verify the user was added to the database
    user = User.query.filter_by(username="testuser").first()
    assert user is not None
    assert user.email == "testuser@example.com"

def test_auth_user(client, sample_user):
    user = User(
        username=sample_user["username"],
        email=sample_user["email"],
        password=sample_user["password"],
        role="ARTIST",
        profile_picture=sample_user["profile_picture"],
        banner=sample_user["banner"]
    )


    import bcrypt
    hash = bcrypt.hashpw(sample_user["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user.password=hash

    db.session.add(user)
    db.session.commit()

    user_login_data = {
        "email":sample_user["email"],
        "password":sample_user["password"]
    }

    response = client.post("/auth/login", json=user_login_data)
    assert response.status_code == 200
    assert "access_token" in response.json

    print(f"Access Token: {response.json["access_token"]}")

    # decode access token to gain user
    from flask_jwt_extended import decode_token
    try:
        decoded_token = decode_token(response.json["access_token"])
        identity = decoded_token.get("sub")
        user = User.query.filter_by(id=int(identity)).first()
        print(f"User from token: {user}")
    except Exception as e:
        print(f"Error decoding access token: {e}")