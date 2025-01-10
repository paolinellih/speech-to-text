from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from domain.schemas.user import UserCreate, UserResponse
from application.use_cases.register_user import RegisterUser
from infrastructure.services.email_service import SMTPEmailService
from infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from infrastructure.database.connection import get_db
from domain.models.user import User
from decouple import config  # To load .env variables

router = APIRouter()

# Initialize your services
db_session = next(get_db())  # Create a session for the DB
user_repository = SQLAlchemyUserRepository(db=db_session)

# Load SMTP configuration from .env file
smtp_host = config("SMTP_HOST")
smtp_port = config("SMTP_PORT", cast=int)  # Ensure it's cast to an integer
smtp_user = config("SMTP_USER")
smtp_password = config("SMTP_PASSWORD")

# Initialize the SMTPEmailService with the loaded configuration
email_service = SMTPEmailService(
    smtp_host=smtp_host,
    smtp_port=smtp_port,
    smtp_user=smtp_user,
    smtp_password=smtp_password,
)

# Pass the repository and email service into the use case
register_user_use_case = RegisterUser(user_repository=user_repository, email_service=email_service)

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the email is already registered
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    # Check if the username is already registered
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists.")
    
    try:
        # Call the use case to register the user and send the confirmation email
        registered_user = register_user_use_case.execute(user.username, user.email, user.password)
    except Exception as e:
        # Handle any exception in the user registration process
        raise HTTPException(status_code=500, detail=f"Failed to register user: {str(e)}")
    
    return registered_user
