from .utils import calculate_upper_bound

def main():
    """
    Main entry point of the program
    """

    test_cases = [
        {"pallet_w": 120, "pallet_l": 100, "box_w": 22, "box_l": 17},
        {"pallet_w": 70, "pallet_l": 60, "box_w": 40, "box_l": 30}
    ]

    for case in test_cases:
        pallet_width, pallet_length = case["pallet_w"], case["pallet_l"]
        box_width, box_length = case["box_w"], case["box_l"]
        print(f"Upper bound for pallet ({pallet_width}x{pallet_length}) and box ({box_width}x{box_length}): {calculate_upper_bound(pallet_width, pallet_length, box_width, box_length)}")

if __name__ == "__main__":
    main()