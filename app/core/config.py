from pydantic import BaseModel, Field
from pathlib import Path

from pydantic_settings import BaseSettings

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "username": "postgres",
    "password": "123",
    "database": "Anime",
    "driver": "postgresql+psycopg2",
}

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expires_minutes: int = 15


class Settings(BaseSettings):
    db_url: str = Field(
        default=f"postgresql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
