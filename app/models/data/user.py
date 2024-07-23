import uuid
from sqlalchemy import Column, String, Boolean
from app.configuration.database import Base
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    password = Column(String)
    type = Column(String, nullable=False)  # 'particular' or 'professional'
    is_active = Column(Boolean, default=True)

    sessions = relationship("Session", back_populates="user")

    __mapper_args__ = {
        'polymorphic_identity': 'base_user',
        'polymorphic_on': type
    }