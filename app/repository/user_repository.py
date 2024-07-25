from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import Depends
from app.configuration.database import get_db
from app.models.data.user import User
from app.models.data.particular_user import ParticularUser
from app.models.data.professional_user import ProfessionalUser
from app.models.requests.user import UserParticular, UserProfessional


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
 
 
    def create_particular(self, user: UserParticular):
        db_user = ParticularUser(**user.model_dump())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def create_professional(self, user: UserProfessional):
        db_user = ProfessionalUser(**user.model_dump())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user(self, user:  UserParticular | UserProfessional):
        pass

    def delete_user(self, user_id: int):
        pass

    def get_all_users(self):
        return self.db.query(User).all()

       
    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def reset_password(self, email: str, new_password: str) -> User:
        user = self.get_user_by_email(email)
        if not user:
            return None

 
        user.password = new_password
        self.db.add(user)  
        self.db.commit()

        return user

    def update_password(self, user: User, new_password: str) -> User:
        user.password = new_password
        self.db.commit()
        
  
        
    