# ------------------------------------------------------------------------
# Filename:    requests.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# Usage: Schemas for Request Data
# 
# DESCRIPTION:
# This module defines the data models (schemas) used for incoming requests to the Text Analysis API. 
# These models leverage Pydantic to ensure that the incoming request data is valid, properly formatted, 
# and adheres to constraints set by the application.
# 
# Schemas:
# - `TextAnalysisRequest`: Represents the data model for text to be analyzed. Includes validation rules 
#   such as minimum and maximum lengths, and checks for URLs in the text.
# - `AnalysisOptions` (if used): Provides finer control over the text analysis by allowing users to specify 
#   which features they want in the analysis (e.g., sentiment analysis, keyword extraction).
# ------------------------------------------------------------------------



from pydantic import BaseModel, validator, constr
from ..core.config import MIN_TEXT_LENGTH, MAX_TEXT_LENGTH


class AnalysisOptions(BaseModel):
    sentiment: bool = True
    summary: bool = True
    keyword_extraction: bool = False


class TextAnalysisRequest(BaseModel):
    text: constr(min_length=MIN_TEXT_LENGTH, max_length=MAX_TEXT_LENGTH, strip_whitespace=True)
    options: AnalysisOptions

    @validator("text")
    def validate_text(cls, value):
        if not value:
            raise ValueError("Text cannot be empty or just whitespace.")
        return value
