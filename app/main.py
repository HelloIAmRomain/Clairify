# ------------------------------------------------------------------------
# Filename:    main.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


from fastapi import FastAPI, HTTPException, Request, Depends
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .routers import analysis
from .core import config
from .core.exceptions import TextAnalyzerBaseException

app = FastAPI()

# Initialize the limiter with a key function to determine the client's IP.
limiter = Limiter(key_func=get_remote_address)

# Add the rate limiter as a dependency for routes.
app.state.limiter = limiter

# Register your routers
app.include_router(analysis.router)


# Exception handler for rate limiting
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

@app.exception_handler(TextAnalyzerBaseException)
async def custom_exception_handler(request: Request, exc: TextAnalyzerBaseException):
    config.logger.error(f"Custom error occurred: {exc.http_exception.detail}")
    raise exc.http_exception

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    config.logger.error(f"HTTP error occurred: {exc.detail}")
    return {"detail": exc.detail}

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    config.logger.error(f"Value error occurred: {str(exc)}")
    return {"detail": str(exc)}
