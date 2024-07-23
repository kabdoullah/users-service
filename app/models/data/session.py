import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from app.configuration.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class Session(Base):
    __tablename__ ='sessions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False) 
    created_at = Column(DateTime, default=None, nullable=True)
    expired_at = Column(DateTime, default=None, nullable=True)
    token = Column(String, default=None, nullable=True)

    users = relationship("User", back_populates="otps")

    