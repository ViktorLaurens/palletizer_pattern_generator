from .utils import Box, Pallet

def main():
    """
    Main entry point of the program
    """
    # Define pallet and box
    pallet = Pallet(120, 100)
    box = Box(22, 17)

    # Run greedy placement
    poses, total_boxes = pallet.place_greedy(box)
    print(f"Total boxes placed: {total_boxes}")

    # Visualize the packing pattern
    pallet.visualize(box, poses)
    
if __name__ == "__main__":
    main()