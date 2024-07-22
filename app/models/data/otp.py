import string
import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from app.configurations.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
from sqlalchemy.dialects.postgresql import UUID


class OTP(Base):
    __tablename__ = 'otp'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    otp_code = Column(String, index=True)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime)
    used = Column(Boolean, default=False)

    users = relationship("User", back_populates="otps")