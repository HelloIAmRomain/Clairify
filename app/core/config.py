# ------------------------------------------------------------------------
# Filename:    __init__.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


import logging
from decouple import config
from slowapi import Limiter
from slowapi.util import get_remote_address

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize the limiter with a key function to determine the client's IP.
limiter = Limiter(key_func=get_remote_address)

TESTING = config('TESTING', default=False, cast=bool)


MAX_TEXT_LENGTH = config('MAX_TEXT_LENGTH', default=1024, cast=int)
MIN_TEXT_LENGTH = config('MIN_TEXT_LENGTH', default=10, cast=int)

MAX_REQUESTS_PER_MINUTE = config('MAX_REQUESTS_PER_MINUTE', default=10, cast=int) if not TESTING else 10000
MAX_REQUESTS_PER_HOUR = config('MAX_REQUESTS_PER_HOUR', default=100, cast=int) if not TESTING else 10000
