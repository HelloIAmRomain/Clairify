# ------------------------------------------------------------------------
# Filename:    main.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

from .core import config
from .core.config import limiter
from .core.exceptions import TextAnalyzerBaseException
from .routers import analysis, auth
from .db.session import engine, Base
import traceback
from app.db.session import SessionLocal
from sqlalchemy.orm import Session


# Database - Create the table
Base.metadata.create_all(bind=engine)


app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add the rate limiter as a dependency for routes.
app.state.limiter = limiter

# Register your routers
app.include_router(analysis.router)
app.include_router(auth.router)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exception(request, exc):
    return HTTPException(
        status_code=429,
        detail="Too Many Requests"
    )


@app.on_event("startup")
async def startup_event():
    config.logger.info("Starting up the application...")


@app.on_event("shutdown")
async def shutdown_event():
    config.logger.info("Shutting down the application...")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return {"detail": "Internal Server Error"}


