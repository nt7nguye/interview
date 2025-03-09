# This file can contain shared fixtures for all tests
import pytest
import random


@pytest.fixture(autouse=True)
def set_random_seed():
    """Set a fixed random seed for reproducible tests"""
    random.seed(42)
