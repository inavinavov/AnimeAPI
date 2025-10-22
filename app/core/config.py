from pydantic import BaseModel
from pathlib import Path

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "username": "postgres",
    "password": "123",
    "database": "Anime",
    "driver": "postgresql+psycopg2"
}

BASE_DIR = Path(__file__).resolve().parent.parent

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    algorithm: str = "RS256"


AuthJWT = AuthJWT()


