from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock
from uuid import uuid4
from app.models.requests.session import SessionCreate


def test_create_session(session_service, session_repo, user_repo):
    user_id = uuid4()
    session_data = SessionCreate(
        user_id=user_id,
        token="test_token",
        expired_at=datetime.now(timezone.utc) + timedelta(days=1)
    )

    user_repo.get_user_by_id.return_value = MagicMock()
    session_repo.create_session.return_value = MagicMock()

    session = session_service.create_session(session_data)

    user_repo.get_user_by_id.assert_called_once_with(user_id)
    session_repo.create_session.assert_called_once_with(session_data)
    assert session is not None
