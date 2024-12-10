from .utils import Box, Pallet, visualize

def main():
    """
    Main entry point of the program
    """
    # Define pallet and box
    pallet = Pallet(70, 60)
    box = Box(40, 30)

    # Run greedy placement
    poses, total_boxes = pallet.place_greedy(box)
    print(f"Total boxes placed: {total_boxes}")

    # Visualize the packing pattern
    visualize(box, poses)

if __name__ == "__main__":
    main()