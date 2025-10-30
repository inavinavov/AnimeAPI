from pydantic import BaseModel, Field
from pathlib import Path

from pydantic_settings import BaseSettings

DB_CONFIG = {
    "driver": "psycopg2",
    "username": "postgres",
    "password": "mypassword",
    "host": "localhost",
    "port": 5432,
    "database": "mydb"
}

DATABASE_URL = f"postgresql+{DB_CONFIG['driver']}://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"


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
