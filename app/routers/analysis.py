# ------------------------------------------------------------------------
# Filename:    analysis.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


from fastapi import APIRouter, Depends
from ..models.text_analysis import analyze_text
from ..schemas import request, response
from ..core import config
from ..core.exceptions import InvalidInputError
from ..main import limiter


router = APIRouter()


@router.post("/analyze", response_model=response.TextAnalysisResponse)
@limiter.limit("5/minute")  # this means the endpoint can be accessed 5 times per minute per client IP.
def analyze_endpoint(request: request.TextAnalysisRequest):
    text = request.text.strip()
    config.logger.info(f"Received a request to analyze a text of length: {len(text)}")
    if not text:
        raise InvalidInputError(detail="Text cannot be empty.")
    result = analyze_text(text)
    config.logger.info("Text analysis completed successfully.")
    return result
