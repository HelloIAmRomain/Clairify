# ------------------------------------------------------------------------
# Filename:    test_main.py
# Copyright (C) 2023 Romain DODET
# Author:      Romain DODET
# ------------------------------------------------------------------------


import pytest
import logging

@pytest.mark.asyncio
async def test_startup_event(caplog, test_app):
    with caplog.at_level(logging.INFO):
        # Get access to the original startup event handlers
        original_startup_handlers = test_app.router.on_startup.copy()

        # Clear the list so they won't be automatically run
        test_app.router.on_startup.clear()

        # Manually run the startup event handlers
        for event_handler in original_startup_handlers:
            await event_handler()

        assert "Starting up the application..." in caplog.text


@pytest.mark.asyncio
async def test_shutdown_event(caplog, test_app):
    with caplog.at_level(logging.INFO):
        # Get access to the original shutdown event handlers
        original_shutdown_handlers = test_app.router.on_shutdown.copy()

        # Clear the list so they won't be automatically run
        test_app.router.on_shutdown.clear()

        # Manually run the shutdown event handlers
        for event_handler in original_shutdown_handlers:
            await event_handler()

        assert "Shutting down the application..." in caplog.text
