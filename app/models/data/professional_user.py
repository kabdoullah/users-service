from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as UUIDType
from .user import User

class ProfessionalUser(User):
    __tablename__ = 'professional_users'

    id = Column(UUIDType(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    number_fix = Column(String, nullable=True)  # Numéro fixe
    phone = Column(String, nullable=True)  # Numéro fixe
    company = Column(String)
    company_type = Column(String)
    country = Column(String)
    professional_category = Column(String)
    sub_category = Column(String, nullable=True)
    website = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'professional_user',
    }