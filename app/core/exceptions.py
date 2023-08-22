# ------------------------------------------------------------------------
# Filename:    __init__.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


from fastapi import HTTPException


class TextAnalyzerBaseException(HTTPException):
    """Base exception for the text analyzer application."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class TextTooLongError(TextAnalyzerBaseException):
    """Exception raised when the input text exceeds the allowed length."""

    def __init__(self, length: int, max_length: int):
        detail = f"Text length of {length} exceeds maximum allowed length of {max_length}."
        super().__init__(status_code=400, detail=detail)


class TextTooShortError(TextAnalyzerBaseException):
    """Exception raised when the input text is too short."""

    def __init__(self, length: int, min_length: int):
        detail = f"Text length of {length} is below allowed length of {min_length}."
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
