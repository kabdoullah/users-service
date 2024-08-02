from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship
from app.configuration.database import Base
import uuid


class Right(Base):
    __tablename__ = 'rights'

    id = Column(UUIDType(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, default=None)

    profiles = relationship(
        "Profile", secondary="profile_rights", back_populates="rights")


class ProfileRight(Base):
    __tablename__ = 'profile_rights'

    profile_id = Column(UUIDType(as_uuid=True), ForeignKey('profiles.id'), primary_key=True)
    right_id = Column(UUIDType(as_uuid=True), ForeignKey('rights.id'), primary_key=True)
