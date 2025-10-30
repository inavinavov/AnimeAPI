from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import DB_CONFIG


DATABASE_URL = f"postgresql+{DB_CONFIG['driver']}://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(engine, expire_on_commit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()