from abc import ABC, abstractmethod

class AuthenticationService(ABC):
    @abstractmethod
    def authenticate(self, email: str, password: str) -> str:
        """
        Authenticate a user and return a JWT token if successful.
        :param email: User's email
        :param password: User's password
        :return: JWT token
        :raises: Exception if authentication fails
        """
        pass
