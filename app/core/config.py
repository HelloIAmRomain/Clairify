# ------------------------------------------------------------------------
# Filename:    __init__.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


import logging
from decouple import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


MAX_TEXT_LENGTH = config('MAX_TEXT_LENGTH', default=1024, cast=int)
MIN_TEXT_LENGTH = config('MIN_TEXT_LENGTH', default=10, cast=int)