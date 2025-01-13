from domain.repositories.user_repository import UserRepository
from utils.hashing import Hasher

class ResetPassword:
    def __init__(self, user_repository: UserRepository, hasher: Hasher):
        self.user_repository = user_repository
        self.hasher = hasher

    def execute(self, token: str, new_password: str):
        print("Token: ", token)
        # Find user by reset token
        user = self.user_repository.get_user_by_reset_token(token)
        if not user:
            raise ValueError("Invalid or expired token.")

        # Hash the new password
        hashed_password = self.hasher.hash_password(new_password)

        # Update the user's password and clear the token
        user.hashed_password = hashed_password
        user.reset_token = None
        self.user_repository.update(user)
