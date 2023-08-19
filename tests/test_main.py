# ------------------------------------------------------------------------
# Filename:    test_main.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


import logging

def test_startup_event(caplog, test_app):
    with caplog.at_level(logging.INFO):
        test_app.router.on_startup.pop()  # We remove the startup event so it can be triggered manually
        test_app.router.run_startup_handlers()
        assert "Starting up the application..." in caplog.text

def test_shutdown_event(caplog, test_app):
    test_app.router.on_shutdown.pop()  # We remove the shutdown event so it can be triggered manually
    test_app.router.run_shutdown_handlers()
    assert "Shutting down the application..." in caplog.text