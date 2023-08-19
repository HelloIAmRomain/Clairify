# ------------------------------------------------------------------------
# Filename:    conftest.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


from fastapi.testclient import TestClient
import pytest
from app.main import app

@pytest.fixture(scope="module")
def test_app():
    return app

@pytest.fixture(scope="module")
def test_client(test_app):
    return TestClient(test_app)