import asyncio

import pytest


@pytest.fixture(scope='session')
def event_loop():
    """Fixture for event loop"""
    return asyncio.new_event_loop()
