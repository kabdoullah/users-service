from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from. user import User

class ParticularUser(User):
    __tablename__ = 'particular'

    id = Column(UUID, ForeignKey('base_users.id'), primary_key=True)
    birth_day = Column(Date)

    _mapper_args_ = {
        'polymorphic_identity': 'particular_user',
    }