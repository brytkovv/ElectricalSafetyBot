import asyncio

import pytest


@pytest.fixture()
def event_loop():
    """Fixture for event loop"""
    return asyncio.new_event_loop()
