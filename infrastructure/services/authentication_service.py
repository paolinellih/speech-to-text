from domain.services.authentication_service import AuthenticationService
from api.utils.jwt_handler import create_access_token
from utils.hashing import Hasher
from domain.repositories.user_repository import UserRepository

class AuthenticationServiceImplementation(AuthenticationService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate(self, email: str, password: str) -> str:
        # Fetch user by email
        user = self.user_repository.get_user_by_email(email)
        if not user or not Hasher.verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password.")

        # Generate and return JWT token with user email in the 'sub' claim
        token = create_access_token({"sub": user.email})
        return token
