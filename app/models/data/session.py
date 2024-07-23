import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship
from app.configuration.database import Base

class Session(Base):
    __tablename__ = 'sessions'

    id = Column(UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUIDType(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=True)
    expired_at = Column(DateTime, default=None, nullable=True)
    token = Column(String, default=None, nullable=True)

    user = relationship("User", back_populates="sessions")
