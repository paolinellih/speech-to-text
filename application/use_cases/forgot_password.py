import uuid
from domain.repositories.user_repository import UserRepository
from infrastructure.services.email_service import SMTPEmailService
from domain.services.encryption_service import EncryptionService
from domain.models.user import User

class ForgotPassword:
    def __init__(self, user_repository: UserRepository, email_service: SMTPEmailService, encryption_service: EncryptionService):
        self.user_repository = user_repository
        self.email_service = email_service
        self.encryption_service = encryption_service

    def execute(self, email: str, reset_link_base: str):
        # Find user by email
        user = self.user_repository.get_user_by_email(email)
        if not user:
            raise ValueError("Email not registered.")

        # Encrypt the user ID
        encrypted_id = self.encryption_service.encrypt(str(user.id))

        # Save reset token to the user object
        user.reset_token = encrypted_id
        self.user_repository.update(user)

        # Compose reset link
        reset_link = f"{reset_link_base}?token={encrypted_id}"

        body = f'Please confirm your email by clicking the link: {reset_link}'

        # Send reset email
        self.email_service.send_email(
            recipient_email=email,
            subject_email='Reset Your Password',
            body_email=body,
        )
