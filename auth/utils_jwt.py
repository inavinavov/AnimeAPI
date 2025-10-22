import hashlib

import bcrypt

import jwt
from app.core.config import AuthJWT


def encode_jwt(
        payload,
        private_key:str=AuthJWT.private_key_path.read_text(),
        algorithm=AuthJWT.ALGORITHM,
):
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm)
    return encoded

def decode_jwt(
        token,
        public_key= AuthJWT.public_key_path.read_text(),
        algorithm=AuthJWT.ALGORITHM,
):
    decoded = jwt.decode(
        token, public_key,
        algorithms=[algorithm])
    return decoded


def hash_password(password:str)->bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

def validate_password(
        password:str,
        hashed_password:bytes)->bool:
    return bcrypt.checkpw(
        password = password.encode(),
        hashed_password = hashed_password
    )
