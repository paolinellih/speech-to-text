from cryptography.fernet import Fernet
from domain.services.encryption_service import EncryptionService
from decouple import config

class FernetEncryptionService(EncryptionService):
    def __init__(self):
        # Load the secret encryption key from environment variables
        self.cipher = Fernet(config("ENCRYPTION_KEY").encode())

    def encrypt(self, plain_text: str) -> str:
        """Encrypts plain text into an encrypted string."""
        return self.cipher.encrypt(plain_text.encode()).decode()

    def decrypt(self, encrypted_text: str) -> str:
        """Decrypts an encrypted string back to plain text."""
        return self.cipher.decrypt(encrypted_text.encode()).decode()
