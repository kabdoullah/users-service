from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import Depends
from app.configuration.database import get_db
from app.models.data.user import User
from app.models.requests.user import UserBase


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
 
 
    def create_user(self, user: UserBase):
        db_user = User(**user.model_dump())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user(self, user: UserBase):
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
        
  
        
    