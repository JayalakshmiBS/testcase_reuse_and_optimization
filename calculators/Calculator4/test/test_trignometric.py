import sys
import os
import pytest
import math
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.calcul_logic import sine, cosine

@pytest.mark.parametrize("angle, expected", [
    (0, 0.0),
    (30, 0.5),
    (90, 1.0),
    (180, 0.0),
    (270, -1.0),
    (360, 0.0)
])
def test_sine_standard_angles(angle, expected):
    assert pytest.approx(sine(angle), abs=1e-4) == expected


@pytest.mark.parametrize("angle, expected", [
    (0, 1.0),
    (60, 0.5),
    (90, 0.0),
    (180, -1.0),
    (270, 0.0),
    (360, 1.0)
])
def test_cosine_standard_angles(angle, expected):
    assert pytest.approx(cosine(angle), abs=1e-4) == expected


@pytest.mark.parametrize("angle, expected", [
    (-30, -0.5),
    (-60, 0.5)
])
def test_negative_angles(angle, expected):
    if angle == -30:
        assert pytest.approx(sine(angle), abs=1e-4) == expected
    else:
        assert pytest.approx(cosine(angle), abs=1e-4) == expected


def test_decimal_angles():
    assert pytest.approx(sine(45.5), abs=1e-7) == math.sin(math.radians(45.5))
    assert pytest.approx(cosine(60.5), abs=1e-7) == math.cos(math.radians(60.5))
