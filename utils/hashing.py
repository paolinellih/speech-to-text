from passlib.context import CryptContext

# Create a CryptContext for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    @staticmethod
    def hash_password(password: str) -> str:
        # Hash the password
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # Verify the password
        return pwd_context.verify(plain_password, hashed_password)
