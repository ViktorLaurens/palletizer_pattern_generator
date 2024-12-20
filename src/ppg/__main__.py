from .utils import Box, Pallet, visualize, visualize_multiple

def main():
    """
    Main function to showcase the palletizing algorithm.
    """
    print("\nWelcome to the Palletizer Program!\n")

    while True:
        print("Choose a configuration to optimize:")
        print("1. Pallet: 120x100 cm, Box: 22x17 cm")
        print("2. Pallet: 120x100 cm, Box: 20x10 cm")
        print("3. Pallet: 70x60 cm, Box: 40x30 cm")
        print("4. Bonus: Two different box sizes (40x30 cm and 22x17 cm)")
        print("0. Exit the program")

        choice = input("\nEnter your choice: ")
        print("\n------------------------------\n")

        if choice == "1":
            pallet = Pallet(120, 100)
            box = Box(22, 17)
        elif choice == "2":
            pallet = Pallet(120, 100)
            box = Box(20, 10)
        elif choice == "3":
            pallet = Pallet(70, 60)
            box = Box(40, 30)
        elif choice == "4":
            # Bonus case with two different box sizes
            pallet = Pallet(120, 100)
            box1 = Box(40, 27)
            box2 = Box(22, 17)

            # Solve for the first box size
            pattern1, total_boxes1 = pallet.place_greedy(box1)
            print(f"First Box (40x30 cm):")
            print(f"Total Boxes Placed: {total_boxes1}")

            # Solve for the second box size in the remaining free space
            free_space_rectangles = pallet.calc_free_space_rectangles(pattern1, box1)
            pattern2 = []
            total_boxes2 = 0

            for rect in free_space_rectangles:
                sub_pallet = Pallet(rect[2], rect[3])  # Width and length of the rectangle
                sub_pattern, sub_total = sub_pallet.place_greedy(box2)
                pattern2.extend([(rect[0] + x, rect[1] + y, theta) for x, y, theta in sub_pattern])
                total_boxes2 += sub_total

            print(f"Second Box (22x17 cm):")
            print(f"Total Boxes Placed: {total_boxes2}")
            
            # Combine and visualize both patterns on a single plot
            visualize_multiple(
                pallet,
                [(box1, pattern1, "blue"), (box2, pattern2, "green")],
                title="Combined Packing Patterns for Two Box Sizes"
            )
            print(f"\nTotal Boxes Placed: {total_boxes1 + total_boxes2}")
            continue # Skip the visualization at the end
        elif choice == "0":
            print("Exiting the program. Goodbye!\n")
            break
        else:
            print("Invalid choice! Please try again.")
            continue # Skip the visualization at the end
        
        # Solve for a single box size
        pattern, total_boxes = pallet.place_greedy(box)
        print(f"Optimal Placement for Box ({box.width}x{box.length} cm):")
        print(f"Total Boxes Placed: {total_boxes}")
        visualize(box, pallet, pattern, title=f"Optimal Placement for Box ({box.width}x{box.length} cm)")
        print("\n------------------------------\n")

if __name__ == "__main__":
    main()