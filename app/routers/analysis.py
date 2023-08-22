# ------------------------------------------------------------------------
# Filename:    analysis.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import uuid
import json


from ..models.text_analysis import analyze_text
from ..schemas.request import TextAnalysisRequest
from ..schemas.response import TextAnalysisResponse
from ..core.config import logger, limiter, MAX_REQUESTS_PER_HOUR, MAX_REQUESTS_PER_MINUTE
from ..core.exceptions import InvalidInputError

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# TODO : Use a database (redis)
analysis_results = {}


@router.post("/analyze", response_model=TextAnalysisResponse)
@limiter.limit(f"{MAX_REQUESTS_PER_MINUTE}/minute")
@limiter.limit(f"{MAX_REQUESTS_PER_HOUR}/hour")
async def analyze_endpoint(request: Request, text_request: TextAnalysisRequest):
    if not text_request.text:
        raise InvalidInputError(detail="Text cannot be empty.")

    text = text_request.text.strip()
    print("text ", text)
    options = text_request.options
    logger.info(f"------- Result dictionary ------- : {text}")
    logger.info(f"------- Options dictionary ------- : {options}")

    logger.info(f"Received a request to analyze a text of length: {len(text)}")

    result = analyze_text(text, options)
    logger.info("Text analysis completed successfully.")
    logger.info(f"------- Result ------- : {result}")
    return {"Result": result}


@router.get("/")
@router.get("/index")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
