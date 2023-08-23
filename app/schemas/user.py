# ------------------------------------------------------------------------
# Filename:    user.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------

# Pydantic models for user schema

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base model for user"""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Model to handle user creation"""
    password: str


class UserLogin(BaseModel):
    """Model to handle user login"""
    username_or_email: str  # Either username or email can be used
    password: str


class User(UserBase):
    """Model to handle full user data"""
    id: int
    created_at: datetime
    last_connexion: datetime

    class Config:
        from_attributes = True
