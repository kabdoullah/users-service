import uuid
from sqlalchemy import Column, DateTime, String, Boolean, Integer, func, ForeignKey, Date, Enum
from app.configuration.database import Base
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship
import enum


class GenderEnum(str, enum.Enum):
    male = "masculin"
    female = "féminin"


class User(Base):
    __tablename__ = 'users'

    id = Column(UUIDType(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    reference = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    profile_id = Column(UUIDType(as_uuid=True), ForeignKey('profiles.id'))
    profile_photo = Column(String, nullable=True)
    birth_day = Column(Date, nullable=True)
    birth_place = Column(String, nullable=True)
    number_fix = Column(String, nullable=True)
    company = Column(String, nullable=True)
    country = Column(String, nullable=True)
    category_id = Column(UUIDType(as_uuid=True),
                         ForeignKey('categories.id'), nullable=True)
    sub_category_id = Column(UUIDType(as_uuid=True),
                             ForeignKey('sub_categories.id'))
    website = Column(String, nullable=True)
    password = Column(String)
    type = Column(String, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=True, default=GenderEnum.male)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    login_attempts = Column(Integer, default=0)
    last_login_attempt = Column(DateTime, default=None)
    last_login = Column(DateTime, default=None)

    profile = relationship("Profile", back_populates="users")
    sessions = relationship("Session", back_populates="users")
    category = relationship("Category", back_populates="users")
    sub_category = relationship("SubCategory", back_populates="users")
