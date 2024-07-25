from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from .user import User

class ParticularUser(User):
    __tablename__ = 'particular_users'

    id = Column(UUIDType(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    birth_day = Column(Date)

    __mapper_args__ = {
        'polymorphic_identity': 'particular_user',
    }