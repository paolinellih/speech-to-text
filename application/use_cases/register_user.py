from domain.services.email_service import EmailService
from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from uuid import uuid4
from utils.hashing import Hasher
from domain.services.encryption_service import EncryptionService
from decouple import config

class RegisterUser:
    def __init__(self, user_repository: UserRepository, email_service: EmailService, encryption_service: EncryptionService):
        self.user_repository = user_repository
        self.email_service = email_service
        self.encryption_service = encryption_service

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

        # Encrypt the user ID
        encrypted_id = self.encryption_service.encrypt(str(user.id))

        user_url = config("USERS_URL");

        # Generate the confirmation link (it could be a token-based URL)
        confirmation_link = f"{user_url}/confirm-email/{encrypted_id}"

        body = f'Please confirm your email by clicking the link: {confirmation_link}'

        # Send the confirmation email
        self.email_service.send_email(
            recipient_email= email, 
            subject_email="Confirm Your Email Address", 
            body_email=body
        )
        
        return user
