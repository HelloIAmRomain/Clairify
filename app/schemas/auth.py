# ------------------------------------------------------------------------
# Filename:    auth.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
