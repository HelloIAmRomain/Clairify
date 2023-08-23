# ------------------------------------------------------------------------
# Filename:    models.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


# SQLAlchemy models for user

from .session import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # Max 50 characters
    email = Column(String(100), unique=True, index=True)  # Max 100 characters
    hashed_password = Column(String(100))  # Max 100 characters
    created_at = Column(DateTime, default=datetime.utcnow)
    last_connexion = Column(DateTime, default=datetime.utcnow)
