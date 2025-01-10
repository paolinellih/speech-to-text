from abc import ABC, abstractmethod
from domain.models.user import User
from typing import Optional

class UserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def save(self, user: User) -> None:
        pass
    
    @abstractmethod
    def update(self, user: User) -> None:
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass
