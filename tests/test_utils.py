"""
Unit tests for utils.py
"""

from src import utils
import pytest


def test_stratospheric_model():
    height = 20000
    temperature, density, sound = utils.stratospheric_model(height)

    assert temperature == pytest.approx(-56.4, abs=0.1)
    assert density == pytest.approx(0.088, abs=0.01)
    assert sound == pytest.approx(294.9, abs=0.1)


def test_tropospheric_model_model():
    height = 0
    temperature, density, sound = utils.tropospheric_model(height)

    assert temperature == pytest.approx(15.04, abs=0.1)
    assert density == pytest.approx(1.22, abs=0.01)
    assert sound == pytest.approx(340.19, abs=0.1)
