# ------------------------------------------------------------------------
# Filename:    test_text_analysis.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------

"""
import pytest
import logging

@pytest.mark.asyncio
async def test_analyze_endpoint(caplog, test_client):
    with caplog.at_level(logging.INFO):
        payload = {
            "text": "This is a good test text.",
            "options": {
                "sentiment": True,
                "summary": True,
                "keyword_extraction": True
            }
        }
        response = test_client.post("/analyze", json=payload)
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_text_too_long_error(caplog, test_client):
    with caplog.at_level(logging.WARNING):
        long_text = "a" * 1001  # Upper limit
        payload = {
            "text": long_text,
            "options": {
                "sentiment": True,
                "summary": True,
                "keyword_extraction": True
            }
        }
        response = test_client.post("/analyze", json=payload)
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_empty_text_error(caplog, test_client):
    with caplog.at_level(logging.WARNING):
        payload = {
            "text": "",
            "options": {
                "sentiment": True,
                "summary": True,
                "keyword_extraction": True
            }
        }
        response = test_client.post("/analyze", json=payload)
        assert response.status_code == 400
"""