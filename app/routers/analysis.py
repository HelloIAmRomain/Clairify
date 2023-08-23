# ------------------------------------------------------------------------
# Filename:    analysis.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------

from typing import Optional

from fastapi import (APIRouter, Depends, Header, HTTPException, Request,
                     Response, status)
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from app.db.crud import get_user_by_username
from app.db.session import get_db
from app.schemas.auth import Token

from ..core.config import (MAX_REQUESTS_PER_HOUR, MAX_REQUESTS_PER_MINUTE,
                           limiter, logger)
from ..core.exceptions import (InvalidInputError, UserNotConnectedError,
                               UserNotFoundError)
from ..core.token_manager import verify_access_token
from ..models.text_analysis import analyze_text
from ..schemas.request import TextAnalysisRequest
from ..schemas.response import TextAnalysisResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to validate the JWT token


def validate_token(authorization: str = Header(...), db: Session = Depends(get_db)):
    print("validate_token")
    print(f"Authorization Header: {authorization}")

    if authorization is None:
        raise UserNotConnectedError("Authorization header missing")

    if not authorization:
        raise UserNotConnectedError()

    token = authorization.split(" ")[1]
    username = verify_access_token(token)

    if username is None:
        raise UserNotConnectedError()

    auth_user = get_user_by_username(db, username)

    if not auth_user:
        raise UserNotConnectedError()

    return auth_user


@router.post("/analyze", response_model=TextAnalysisResponse)
@limiter.limit(f"{MAX_REQUESTS_PER_MINUTE}/minute")
@limiter.limit(f"{MAX_REQUESTS_PER_HOUR}/hour")
async def analyze_endpoint(request: Request, text_request: TextAnalysisRequest, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    
    if not access_token:
        raise HTTPException(status_code=401, detail="User not authenticated")
        
    try:
        username = verify_access_token(access_token)
        if username is None:
            raise HTTPException(status_code=401, detail="Could not extract user from token")
        
        user = get_user_by_username(db, username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
            
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not text_request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    text = text_request.text.strip()
    options = text_request.options
    logger.info(f"Received a request from {user.username} to analyze a text of length: {len(text)}")

    result = analyze_text(text, options)
    logger.info("Text analysis completed successfully.")

    return {"Result": result}



@router.get("/app")
async def read_app(request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    
    if not access_token:
        raise HTTPException(status_code=401, detail="User not authenticated")

    try:
        username = verify_access_token(access_token)
        if username is None:
            raise HTTPException(status_code=401, detail="Could not extract user from token")


        # Fetch the user based on the decoded username
        user = get_user_by_username(db, username)
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    return templates.TemplateResponse("app.html", {"request": request, "user": user})

