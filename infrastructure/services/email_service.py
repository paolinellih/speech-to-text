import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from domain.services.email_service import EmailService

class SMTPEmailService(EmailService):
    def __init__(self, smtp_host: str, smtp_port: int, smtp_user: str, smtp_password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def send_confirmation_email(self, recipient_email: str, confirmation_link: str):
        # Compose the email message
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user  # From is your Gmail address
        msg['To'] = recipient_email  # To is the recipient's address
        msg['Subject'] = 'Confirm Your Email Address'

        body = f'Please confirm your email by clicking the link: {confirmation_link}'

        msg.attach(MIMEText(body, 'plain'))

        try:
            print("Attempting to send email...")
            print(f"SMTP configuration: {self.smtp_host}, {self.smtp_port}, {self.smtp_user}")
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                print("SMTP server connection successful.")
                server.starttls()  # Make sure TLS is used
                server.login(self.smtp_user, self.smtp_password)
                text = msg.as_string()
                server.sendmail(self.smtp_user, recipient_email, text)
                print(f'Confirmation email sent to {recipient_email}')
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
