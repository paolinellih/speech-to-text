from abc import ABC, abstractmethod

class EmailService(ABC):
    @abstractmethod
    def send_email(self, recipient_email: str, subject_email: str, body_email: str):
        pass