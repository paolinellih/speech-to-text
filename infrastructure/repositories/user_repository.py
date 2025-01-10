from typing import Optional
from domain.repositories.user_repository import UserRepository
from domain.models.user import User
from sqlalchemy.orm import Session

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def save(self, user: User) -> None:
        self.db.add(user)
        self.db.commit()
    
    def update(self, user: User) -> None:
        self.db.merge(user)
        self.db.commit()
    
    def delete(self, user_id: int) -> None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
