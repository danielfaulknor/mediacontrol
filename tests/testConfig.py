import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from lib.config import config
from nose.tools import *


def test_existing_config():
    assert config.get("test", "test") == "testingconfig"


def test_missing_config():
    try:
        config.get("test", "noexistent")
        assert False
    except:
        assert True


def test_create_config():
    config.set("test", "test2", "testingconfig2")
    assert config.get("test", "test2") == "testingconfig2"
