from domain.services.email_service import EmailService
from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from uuid import uuid4
from utils.hashing import Hasher

class RegisterUser:
    def __init__(self, user_repository: UserRepository, email_service: EmailService):
        self.user_repository = user_repository
        self.email_service = email_service

    def execute(self, username: str, email: str, password: str):
        # Hash the password before saving it
        hashed_password = Hasher.hash_password(password)

        # Logic to create the user (now with hashed password)
        user = User(
            id=str(uuid4()),  # assuming UUID for user ID
            username=username,
            email=email,
            hashed_password=hashed_password,  # Hashed password now
        )

        # Save the user to the repository
        self.user_repository.save(user)

        # Generate the confirmation link (it could be a token-based URL)
        confirmation_link = f"http://example.com/confirm_email/{user.id}"

        # Send the confirmation email
        self.email_service.send_confirmation_email(email, confirmation_link)
        
        return user
