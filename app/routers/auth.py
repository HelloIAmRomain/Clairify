# ------------------------------------------------------------------------
# Filename:    auth.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


import logging
from typing import Dict

from fastapi import (APIRouter, Depends, Header, HTTPException, Request,
                     Response, status)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.exceptions import (EmailAlreadyExistsError, InvalidPasswordError,
                                 UsernameAlreadyExistsError, UserNotFoundError)
from app.core.token_manager import (create_access_token, create_refresh_token,
                                    verify_access_token)
from app.db.crud import (create_user, get_user_by_email, get_user_by_username,
                         verify_password)
from app.db.session import get_db
from app.schemas.auth import Token
from app.schemas.user import User, UserCreate, UserLogin
from fastapi.responses import RedirectResponse


logging.basicConfig(level=logging.INFO)


router = APIRouter()
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get("/")
@router.get("/index")
@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_model=Token)
async def login_for_access_token(response: Response, form_data: UserLogin, db: Session = Depends(get_db)):
    print("login_function")

    # Query by both username and email to find the user
    user_by_username = get_user_by_username(db, form_data.username_or_email)
    user_by_email = get_user_by_email(db, form_data.username_or_email)

    user = user_by_username or user_by_email

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token_data = {"sub": user.username, "type": "access"}
    refresh_token_data = {"sub": user.username, "type": "refresh"}

    access_token = create_access_token(access_token_data)
    refresh_token = create_refresh_token(refresh_token_data)

    # Setting the HTTP-Only cookie with the access token
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,
        max_age=1800,  # Expiry time in seconds
        # secure=True,  # Uncomment this line for HTTPS
    )

    return {"access_token": access_token, "token_type": "Bearer", "refresh_token": refresh_token}


@router.post("/refresh", response_model=Token)
async def refresh(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("refresh")
    payload = verify_access_token(token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    current_user = payload["sub"]
    new_access_token_data = {"sub": current_user, "type": "access"}
    new_access_token = create_access_token(new_access_token_data)

    return {"access_token": new_access_token}


@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register_function(new_user: UserCreate, db: Session = Depends(get_db)):

    # No need to parse it into JSON here since new_user is already parsed

    # Check if username exists
    existing_user = get_user_by_username(db, new_user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail={
                            "error": "Username already exists"})

    # Check if email exists
    existing_email = get_user_by_email(db, new_user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail={
                            "error": "Email already exists"})

    # Create new user and return ID
    id_user = create_user(db, new_user)
    return JSONResponse(content={"id": id_user}, status_code=201)


@router.post("/logout")
async def logout(response: Response, db: Session = Depends(get_db)):
    # TODO : invalidate token
    
    # Remove the cookie on the client's side
    response.delete_cookie("access_token")
    
    # Return a JSON response
    return {"detail": "Successfully logged out"}