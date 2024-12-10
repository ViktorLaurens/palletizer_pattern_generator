def calculate_upper_bound(pallet_width, pallet_length, box_width, box_length):
    """
    Calculate the upper bound for the number of boxes that can fit on the pallet.
    """
    pallet_area = pallet_width * pallet_length
    box_area = box_width * box_length
    return pallet_area // box_area
