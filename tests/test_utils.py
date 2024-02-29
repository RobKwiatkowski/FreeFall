"""
Unit tests for utils.py
"""

from src.free_fall import utils
import pytest


def test_stratospheric_model():
    height = 20000
    air = utils.stratospheric_model(height)

    assert air["temp_c"] == pytest.approx(-56.4, abs=0.1)
    assert air["density"] == pytest.approx(0.088, abs=0.01)
    assert air["sound"] == pytest.approx(294.9, abs=0.1)


def test_tropospheric_model_model():
    height = 0
    air = utils.tropospheric_model(height)

    assert air["temp_c"] == pytest.approx(15.04, abs=0.1)
    assert air["density"] == pytest.approx(1.22, abs=0.01)
    assert air["sound"] == pytest.approx(340.19, abs=0.1)


def test_atmosphere_model():
    height = 20000
    air = utils.atmosphere_model(height)

    assert air["temp_c"] == pytest.approx(-56.4, abs=0.1)
    assert air["density"] == pytest.approx(0.088, abs=0.01)
    assert air["sound"] == pytest.approx(294.9, abs=0.1)
