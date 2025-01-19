from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from application.use_cases.register_user import RegisterUser
from application.use_cases.reset_password import ResetPassword
from application.use_cases.forgot_password import ForgotPassword
from application.use_cases.reset_password import ResetPassword
from application.use_cases.login_use_case import LoginUser
from domain.schemas.user import ForgotPasswordRequest, ResetPasswordRequest, LoginRequest
from domain.schemas.user import UserCreate, UserResponse, LoginResponse
from infrastructure.services.email_service import SMTPEmailService
from infrastructure.services.fernet_encryption_service import FernetEncryptionService
from infrastructure.services.authentication_service import AuthenticationServiceImplementation
from infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from infrastructure.database.connection import get_db
from domain.models.user import User
from decouple import config
from utils.hashing import Hasher
from api.utils.jwt_handler import create_access_token
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()

# Initialize your services
db_session = next(get_db())  # Create a session for the DB
user_repository = SQLAlchemyUserRepository(db=db_session)
encryption_service = FernetEncryptionService()
authentication_service = AuthenticationServiceImplementation(user_repository)

# Load SMTP configuration from .env file
smtp_host = config("SMTP_HOST")
smtp_port = config("SMTP_PORT", cast=int)  # Ensure it's cast to an integer
smtp_user = config("SMTP_USER")
smtp_password = config("SMTP_PASSWORD")

users_url = config("USERS_URL")

# Initialize the SMTPEmailService with the loaded configuration
email_service = SMTPEmailService(
    smtp_host=smtp_host,
    smtp_port=smtp_port,
    smtp_user=smtp_user,
    smtp_password=smtp_password,
)

# Pass the repository and email service into the use case
register_user_use_case = RegisterUser(
    user_repository=user_repository, 
    email_service=email_service, 
    encryption_service=encryption_service
)

forgot_password_use_case = ForgotPassword(user_repository, email_service, encryption_service)
reset_password_use_case = ResetPassword(user_repository, Hasher())
login_user_use_case = LoginUser(authentication_service)


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # # Check if the email is already registered
    # existing_user = db.query(User).filter(User.email == user.email).first()
    # if existing_user:
    #     return existing_user
    #     #raise HTTPException(status_code=400, detail="Email already registered.")
    
    # # Check if the username is already registered
    # existing_username = db.query(User).filter(User.username == user.username).first()
    # if existing_username:
    #     return existing_user
    #     #raise HTTPException(status_code=400, detail="Username already exists.")
    
    try:
        # Call the use case to register the user and send the confirmation email
        registered_user = register_user_use_case.execute(user.username, user.email, user.password)
    except Exception as e:
        # Handle any exception in the user registration process
        raise HTTPException(status_code=500, detail=f"Failed to register user: {str(e)}")
    
    return registered_user

@router.get("/confirm-email/{encrypted_id}")
def confirm_email(request: Request, encrypted_id: str):
    try:
        # Decrypt the user ID
        user_id = encryption_service.decrypt(encrypted_id)

        # Find and update the user
        user = db_session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        user.is_email_verified = True
        db_session.commit()
        return templates.TemplateResponse("email_confirmation.html", {"request": request})
        #return {"message": "Email confirmed successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid or expired link: {str(e)}")

@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

@router.post("/forgot-password")
def forgot_password(request: Request, forgot_password_request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    try:
        reset_link_base = f"{users_url}/reset-password"
        forgot_password_use_case.execute(email=forgot_password_request.email, reset_link_base=reset_link_base)
        return templates.TemplateResponse("forgot_password_confirmation.html", {"request": request})
        #return {"message": "Password reset email sent successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request, token: str):
    return templates.TemplateResponse("reset_password.html", {"request": request, "token": token})

@router.post("/reset-password")
def reset_password(request: Request, reset_password_request: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        reset_password_use_case.execute(token=reset_password_request.token, new_password=reset_password_request.new_password)
        return templates.TemplateResponse("reset_password_confirmation.html", {"request": request})
        #return {"message": "Password reset successful."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login", response_model=LoginResponse)
def login_user(login_request: LoginRequest, db: Session = Depends(get_db)):
    try:
        encrypted_token = login_user_use_case.execute(login_request.email, login_request.password)
        return {"access_token": encrypted_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))