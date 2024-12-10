import pytest
from ppg.utils import calculate_upper_bound

def test_calculate_upper_bound():
    # Test Case 1: Pallet and box dimensions fit perfectly
    pallet_width, pallet_length = 120, 100  # in cm
    box_width, box_length = 20, 10  # in cm
    assert calculate_upper_bound(pallet_width, pallet_length, box_width, box_length) == 60

    # Test Case 2: Box dimensions do not perfectly divide the pallet area
    pallet_width, pallet_length = 123, 98  # in cm
    box_width, box_length = 22, 17  # in cm
    assert calculate_upper_bound(pallet_width, pallet_length, box_width, box_length) == 32

    # Test Case 3: Box larger than pallet
    pallet_width, pallet_length = 50, 50  # in cm
    box_width, box_length = 60, 60  # in cm
    assert calculate_upper_bound(pallet_width, pallet_length, box_width, box_length) == 0

    # Test Case 4: Exact fit with rotation
    pallet_width, pallet_length = 100, 40  # in cm
    box_width, box_length = 20, 40  # in cm
    assert calculate_upper_bound(pallet_width, pallet_length, box_width, box_length) == 5

    # Test Case 5: Both pallet and box are squares
    pallet_width, pallet_length = 100, 100  # in cm
    box_width, box_length = 20, 20  # in cm
    assert calculate_upper_bound(pallet_width, pallet_length, box_width, box_length) == 25
