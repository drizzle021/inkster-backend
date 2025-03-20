import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    app = create_app(config_class="app.config.TestingConfig")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
