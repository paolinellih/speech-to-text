from api.api import app
from database.connection import Base, engine
from database.models import user
import uvicorn

if __name__ == "__main__":
    database_url = os.getenv("DATABASE_URL")
    print(f"Connecting to database at {database_url}")

    # Create all tables in the database
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

    # Start the FastAPI app using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# To generate a secret key:
#import secrets
#print(secrets.token_urlsafe(32))

# to generate Encryption Key:
#python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"