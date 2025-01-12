from abc import ABC, abstractmethod

class EncryptionService(ABC):
    @abstractmethod
    def encrypt(self, plain_text: str) -> str:
        """Encrypts a plain text string and returns the encrypted value."""
        pass

    @abstractmethod
    def decrypt(self, encrypted_text: str) -> str:
        """Decrypts an encrypted string and returns the plain text value."""
        pass
