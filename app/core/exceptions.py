# ------------------------------------------------------------------------
# Filename:    __init__.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


from fastapi import HTTPException

class TextAnalyzerBaseException(Exception):
    """Base exception for the text analyzer application."""

    def __init__(self, status_code: int, detail: str):
        self.http_exception = HTTPException(status_code=status_code, detail=detail)
        super().__init__(detail)

class TextTooLongError(TextAnalyzerBaseException):
    """Exception raised when the input text exceeds the allowed length."""
    
    def __init__(self, length: int, max_length: int):
        self.max_length = max_length
        detail = f"Text length of {length} exceeds maximum allowed length of {max_length}."
        super().__init__(status_code=400, detail=detail)

class ModelInferenceError(TextAnalyzerBaseException):
    """Exception raised when there's an error during model inference."""
    
    def __init__(self, model_name: str):
        detail = f"Error occurred during inference with {model_name} model."
        super().__init__(status_code=500, detail=detail)

class InvalidInputError(TextAnalyzerBaseException):
    """Exception raised for invalid input data."""

    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)
