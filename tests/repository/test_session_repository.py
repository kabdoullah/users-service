from datetime import datetime, timedelta, timezone
from uuid import uuid4
from app.models.requests.session import SessionCreate


def test_create_session(session_repo):
    session_data = SessionCreate(
        user_id=uuid4(),
        token="test_token",
        expired_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    session = session_repo.create_session(session_data)
    assert session is not None
    assert session.token == "test_token"
    

def test_get_session(session_repo):
    session_data = SessionCreate(
        user_id=uuid4(),
        token="test_token",
        expired_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    created_session = session_repo.create_session(session_data)
    retrieved_session = session_repo.get_session(created_session.id)
    assert retrieved_session is not None
    assert retrieved_session.token == "test_token"
    
def test_delete_session(session_repo):
    session_data = SessionCreate(
        user_id=uuid4(),
        token="test_token",
        expired_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    created_session = session_repo.create_session(session_data)
    assert session_repo.delete_session(created_session.id) is True
    assert session_repo.get_session(created_session.id) is None

def test_get_sessions_by_user(session_repo):
    user_id = uuid4()
    session_data1 = SessionCreate(
        user_id=user_id,
        token="test_token_1",
        expired_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    session_data2 = SessionCreate(
        user_id=user_id,
        token="test_token_2",
        expired_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    session_repo.create_session(session_data1)
    session_repo.create_session(session_data2)
    
    sessions = session_repo.get_sessions_by_user(user_id)
    assert len(sessions) == 2
    assert all(session.token in ["test_token_1", "test_token_2"] for session in sessions)