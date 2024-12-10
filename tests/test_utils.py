import pytest
from ppg.utils import Box, Pallet

def test_calculate_upper_bound():
    """Test the calculate_upper_bound method."""
    # Create a pallet and a box
    pallet = Pallet(120, 100)  # Pallet dimensions: 120x100
    box = Box(20, 10)  # Box dimensions: 20x10

    # Calculate the upper bound
    expected_upper_bound = 60  # Pallet area / Box area
    assert pallet.calculate_upper_bound(box) == expected_upper_bound
    # change
    pallet = Pallet(123, 98)  # Pallet dimensions: 120x100
    box = Box(21, 10)  # Box dimensions: 20x10

    # Calculate the upper bound
    expected_upper_bound = 57  # Pallet area / Box area
    assert pallet.calculate_upper_bound(box) == expected_upper_bound

@pytest.mark.parametrize(
    "rect, box_dim, expected",
    [
        ((0, 0, 50, 50), (20, 20), True),  # Box fits without rotation
        ((0, 0, 50, 50), (60, 40), False),  # Box too wide
        ((0, 0, 50, 50), (40, 60), False),  # Box too tall
        ((0, 0, 50, 50), (30, 40), True),  # Box fits without rotation
        ((0, 0, 35, 50), (40, 30), True),  # Box fits with rotation
        ((0, 0, 30, 30), (40, 20), False),  # Box too wide or tall
    ],
)
def test_check_free_space_rectangle(rect, box_dim, expected):
    """Test the check_free_space_rectangle method with various scenarios."""
    pallet = Pallet(120, 100)  # Pallet dimensions are irrelevant for this test
    box = Box(*box_dim)
    assert pallet.check_free_space_rectangle(rect, box) == expected

def test_calc_free_space_rectangles():
    """Test the calc_free_space_rectangles method."""
    # Create a pallet and a box
    pallet = Pallet(120, 100)
    box = Box(20, 10)

    # Define the pattern of placed boxes
    pattern = [
        (0, 0, 0),  # Box at (0, 0), no rotation
        (20, 0, 0),  # Box at (20, 0), no rotation
        (40, 0, 0),  # Box at (40, 0), no rotation
    ]

    # Expected results
    max_x = 40 + box.width  # Last box's x position + width
    max_y = 0 + box.length  # Last box's y position + length
    expected_above = (0, max_y, pallet.width, pallet.length - max_y)
    expected_right = (max_x, 0, pallet.width - max_x, pallet.length)

    # Call the method
    free_rectangles = pallet.calc_free_space_rectangles(pattern, box)

    # Check the results
    assert len(free_rectangles) == 2
    assert free_rectangles[0] == expected_above
    assert free_rectangles[1] == expected_right

def test_calc_usable_space():
    """Test the calc_usable_space method."""
    # Create a pallet and a box
    pallet = Pallet(120, 100)
    box = Box(20, 10)

    # Define the pattern of placed boxes
    pattern = [
        (0, 0, 0),  # Box at (0, 0), no rotation
        (20, 0, 0),  # Box at (20, 0), no rotation
    ]

    # Mock the calc_free_space_rectangles and check_free_space_rectangle methods
    pallet.calc_free_space_rectangles = lambda pattern, box: [
        (40, 0, 80, 100),  # Remaining space to the right
        (0, 10, 120, 90),  # Remaining space above
    ]
    pallet.check_free_space_rectangle = lambda rect, box: True

    # Calculate the expected usable space
    box_area = box.width * box.length
    used_space = len(pattern) * box_area
    free_space = (80 * 100) + (120 * 90)  # Areas of the two free rectangles
    expected_usable_space = used_space + free_space

    # Call the method
    usable_space = pallet.calc_usable_space(pattern, box)

    # Check the result
    assert usable_space == expected_usable_space

def test_place_greedy():
    """Test the place_greedy method."""
    # Create a pallet and a box
    pallet = Pallet(120, 100)
    box = Box(20, 10)

    # Call the method
    pattern, total_boxes = pallet.place_greedy(box)

    # Expected results
    max_boxes = (120 // box.width) * (100 // box.length)  # Full pallet
    assert total_boxes == max_boxes
    assert len(pattern) == max_boxes
    for x, y, theta in pattern:
        assert 0 <= x < 120
        assert 0 <= y < 100
        assert theta in {0, 90}  # Ensure valid rotations


