# ------------------------------------------------------------------------
# Filename:    test_text_analysis.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


import logging

def test_startup_and_shutdown_events(caplog, test_app):
    with caplog.at_level(logging.INFO):
        test_app.router.on_startup.pop()  # We remove the startup event so it can be triggered manually
        test_app.router.on_shutdown.pop()  # We remove the shutdown event so it can be triggered manually

        test_app.router.run_startup_handlers()
        assert "Starting up the application..." in caplog.text

        test_app.router.run_shutdown_handlers()
        assert "Shutting down the application..." in caplog.text

def test_analyze_endpoint(test_client):
    response = test_client.post("/analyze", json={"text": "This is a test text."})
    assert response.status_code == 200
    # More assertions based on expected response...

def test_text_too_long_error(test_client):
    long_text = "a" * 1001  # Assuming your limit is 1000 characters
    response = test_client.post("/analyze", json={"text": long_text})
    assert response.status_code == 400
    assert "exceeds maximum allowed length" in response.json()["detail"]

def test_invalid_input_error(test_client):
    response = test_client.post("/analyze", json={})
    assert response.status_code == 400
    assert "Text cannot be empty." in response.json()["detail"]
