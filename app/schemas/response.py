# ------------------------------------------------------------------------
# Filename:    response.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# Usage: Schemas for Request Data
#
# DESCRIPTION:
# Schemas for Response Data
#
# This module defines the data models (schemas) used for outgoing responses from the Text Analysis API.
# These models ensure consistency in the data returned to the client and help in auto-generating
# documentation for the API, thanks to FastAPI's integration with Pydantic.
#
# Schemas:
# - `TextAnalysisResponse`: Represents the data model for the results of the text analysis. This includes
#   fields like summary, sentiment score, and potential keyword extraction results.
# ------------------------------------------------------------------------


from typing import Optional, List
from pydantic import BaseModel, Field


class TextAnalysis(BaseModel):
    summary: Optional[str] = Field(None)
    sentiment: Optional[str] = Field(None)
    score: Optional[float] = Field(None)
    keywords: Optional[List[str]] = Field(None)


class TextAnalysisResponse(BaseModel):
    Result: TextAnalysis
