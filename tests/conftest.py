import mock
import pytest
import sys


@pytest.fixture
def neopixel():
    neopixel = mock.MagicMock()
    sys.modules['neopixel'] = neopixel
    yield neopixel
    del sys.modules['neopixel']


@pytest.fixture
def micropython():
    micropython = mock.Mock()
    micropython.const = lambda x: x
    sys.modules['micropython'] = micropython
    yield micropython
    del sys.modules['micropython']


@pytest.fixture
def digitalio():
    digitalio = mock.Mock()
    sys.modules['digitalio'] = digitalio
    yield digitalio
    del sys.modules['digitalio']
