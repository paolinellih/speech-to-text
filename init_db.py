from sqlalchemy import create_engine
from domain.models.user import Base
from infrastructure.database.connection import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
print("Tables created.")