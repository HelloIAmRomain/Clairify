# ------------------------------------------------------------------------
# Filename:    token_manager.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


from datetime import datetime, timedelta
from typing import Optional

from jose import ExpiredSignatureError, JWTError, jwt

from .config import (ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, DOMAIN_NAME,
                     REFRESH_TOKEN_EXPIRE_MINUTES, SECRET_KEY)


def create_access_token(data: dict) -> str:
    """
    Create a new access token.

    :param data: A dictionary containing claims like "sub" (subject/user ID).
    :return: A JWT encoded as a string.
    """
    print("create_access_token")
    to_encode = data.copy()
    to_encode.update({"domain_name": DOMAIN_NAME})
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    print("create_refresh_token")
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "domain": DOMAIN_NAME})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> Optional[str]:
    """
    Verify an access token and return the username if successful.

    :param token: A JWT encoded as a string.
    :return: The username from the token or None if verification fails.
    """
    print("verify_access_token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        domain_name: str = payload.get("domain_name")
        print("payload", payload)

        if username is None or domain_name != DOMAIN_NAME:
            return None
        return username
    except ExpiredSignatureError:
        print("Token has expired")
        return None
    except JWTError:
        print("Invalid token")
        return None
