from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .user import User

class ProfessionalUser(User):
    __tablename__ = 'professional'

    id = Column(UUID, ForeignKey('base_users.id'), primary_key=True)
    phone_2 = Column(String, nullable=True)  # Numéro fixe
    company = Column(String)
    country = Column(String)
    company_type = Column(String)
    professional_category = Column(String)
    sub_category = Column(String, nullable=True)
    website = Column(String, nullable=True)

    _mapper_args_ = {
        'polymorphic_identity': 'professional_user',
    }
