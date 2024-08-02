import uuid
from sqlalchemy import Column, String, ForeignKey
from app.configuration.database import Base
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = 'categories'

    id = Column(UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="category")
    sub_categories = relationship("SubCategory", back_populates="category")


class SubCategory(Base):
    __tablename__ = 'sub_categories'

    id = Column(UUIDType(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category_id = Column(UUIDType(as_uuid=True), ForeignKey('categories.id'))

    category = relationship("Category", back_populates="sub_categories")
    users = relationship("User", back_populates="sub_category")
