import asyncio

import pytest


# TODO: ошибка закрытия эвент лупа
@pytest.fixture(scope='session')
def event_loop():
    """Fixture for event loop"""
    return asyncio.new_event_loop()
