from fastapi import Response, Request
from user_service.config import settings
from datetime import datetime, timedelta
from typing import Any, Union
import jwt


def create_access_token(subject: Union[str, Any], scopes: list[str] = None, expires_delta: timedelta = None, request: Request = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    if request:
        request.session['scopes'] = scopes or []
        request.session['sub'] = str(subject)
    else:
        to_encode['scopes'] = scopes or [] 
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str, request: Request) -> dict:
    try:
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        scopes = request.session.get("scopes", [])
        decoded_jwt['scopes'] = scopes
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def set_jwt_cookie(response: Response, cookie_name: str, encoded_jwt: str, expiration: datetime, secure = True):
    response.set_cookie(key=cookie_name, value=encoded_jwt, httponly=True, expires=expiration.strftime("%a, %d %b %Y %H:%M:%S GMT"), secure=secure, samesite="lax")