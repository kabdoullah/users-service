from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.user_service import UserService
from app.services.session_service import SessionService
from app.models.data.user import User
from app.models.requests.session import SessionCreate
from sqlalchemy import create_engine
from app.configuration.database import Base
from sqlalchemy.orm import sessionmaker
from app.repository.session_repository import SessionRepository



# Création d'une base de données SQLite en mémoire pour les tests
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture
def test_db():
    db = TestingSessionLocal()
    Base.metadata.create_all(bind=engine)
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def session_repo(test_db):
    return SessionRepository(db=test_db)



mock_user = User(id=str(uuid4()), email="test@example.com", password="hashedpassword", is_active=True)

# Mock user service
class MockUserService(UserService):
    def authenticate_user(self, email: str, password: str):
        if email == "test@example.com" and password == "correctpassword":
            return mock_user
        return None

# Mock session service
class MockSessionService(SessionService):
    def create_session(self, session_data: SessionCreate):
        return

@pytest.fixture(scope="module")
def test_client():
    # Dependency overrides
    app.dependency_overrides[UserService] = lambda: MockUserService()
    app.dependency_overrides[SessionService] = lambda: MockSessionService()
    
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
def mock_user_data():
    return mock_user

