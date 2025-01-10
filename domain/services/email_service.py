from abc import ABC, abstractmethod

class EmailService(ABC):
    @abstractmethod
    def send_confirmation_email(self, recipient_email: str, confirmation_link: str):
        pass