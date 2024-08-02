from sqlalchemy import Column, DateTime, String, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship
from app.configuration.database import Base
import uuid


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, default=None)

    rights = relationship("Right", secondary="profile_rights", back_populates="profiles")
    users = relationship("User", back_populates="profile")
