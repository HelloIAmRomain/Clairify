# ------------------------------------------------------------------------
# Filename:    test_exceptions.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


import pytest
from app.core.exceptions import (
    TextAnalyzerBaseException,
    TextTooLongError,
    ModelInferenceError,
    InvalidInputError
)

def test_text_too_long_error_exception():
    max_length = 1000
    too_long_text_length = 1100
    with pytest.raises(TextTooLongError) as exc_info:
        raise TextTooLongError(too_long_text_length, max_length)
    assert f"{too_long_text_length} exceeds maximum allowed length of {max_length}" in str(exc_info.value)

def test_model_inference_error_exception():
    with pytest.raises(ModelInferenceError) as exc_info:
        raise ModelInferenceError("BART Summarizer")
    assert "Error occurred during inference with BART Summarizer model" in str(exc_info.value)

def test_invalid_input_error_exception():
    with pytest.raises(InvalidInputError) as exc_info:
        raise InvalidInputError("Text cannot be empty.")
    assert "Text cannot be empty." in str(exc_info.value)

def test_base_exception_is_abstract():
    with pytest.raises(TypeError):
        _ = TextAnalyzerBaseException()

def test_custom_exceptions_inherit_correctly():
    assert issubclass(TextTooLongError, TextAnalyzerBaseException)
    assert issubclass(ModelInferenceError, TextAnalyzerBaseException)
    assert issubclass(InvalidInputError, TextAnalyzerBaseException)

# Optionally, add any more tests for other exceptions or behaviors you have or will add.
