from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.utils.jwt_handler import verify_access_token

# Create an instance of HTTPBearer for Bearer token support
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials  # Extract the token from the Authorization header
    payload = verify_access_token(token)  # Validate and decode the token

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Return the user's email (or other identifier) from the token payload
    return payload["sub"]
