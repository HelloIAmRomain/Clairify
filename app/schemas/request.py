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


from pydantic import BaseModel, field_validator, constr
from ..core.config import MIN_TEXT_LENGTH, MAX_TEXT_LENGTH


class AnalysisOptions(BaseModel):
    sentiment: bool = True
    summary: bool = True
    keyword_extraction: bool = True


class TextAnalysisRequest(BaseModel):
    text: constr(strip_whitespace=True)
    options: AnalysisOptions

    @field_validator("text")  # Validation of the "text" values
    def validate_text(cls, value):
        if not value:
            raise ValueError("Text cannot be empty or just whitespaces.")
        return value
