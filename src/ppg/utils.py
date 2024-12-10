import matplotlib.pyplot as plt

class Box:
    """Represents a box with dimensions width (w) and length (l)."""
    def __init__(self, width, length):
        self.width = width
        self.length = length


class Pallet:
    """Represents a pallet with dimensions width (W) and length (L)."""
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.free_rectangles = [(0, 0, width, length)]  # Initially, the entire pallet is free

    def place_greedy(self, box):
        """
        Place boxes on the pallet using a greedy search.

        Args:
            box (Box): The box to place.

        Returns:
            list: List of tuples representing the poses (x, y, theta).
            int: Total number of boxes placed.
        """
        poses = []
        total_boxes = 0

        while True:
            # Find the best placement for the box
            best_rect = None
            best_orientation = None
            min_waste = float('inf')

            for rect in self.free_rectangles:
                x, y, rect_w, rect_l = rect

                # Try placing the box without rotation
                if rect_w >= box.width and rect_l >= box.length:
                    waste = (rect_w - box.width) * rect_l + rect_w * (rect_l - box.length)
                    if waste < min_waste:
                        min_waste = waste
                        best_rect = rect
                        best_orientation = (box.width, box.length, 0)

                # Try placing the box with rotation
                if rect_w >= box.length and rect_l >= box.width:
                    waste = (rect_w - box.length) * rect_l + rect_w * (rect_l - box.width)
                    if waste < min_waste:
                        min_waste = waste
                        best_rect = rect
                        best_orientation = (box.length, box.width, 90)

            # If no placement is found, terminate
            if not best_rect:
                break

            # Place the box
            x, y, rect_w, rect_l = best_rect
            box_w, box_l, theta = best_orientation
            poses.append((x, y, theta))
            total_boxes += 1

            # Split the rectangle into smaller rectangles
            self.free_rectangles.remove(best_rect)
            if rect_w > box_w:
                self.free_rectangles.append((x + box_w, y, rect_w - box_w, rect_l))
            if rect_l > box_l:
                self.free_rectangles.append((x, y + box_l, box_w, rect_l - box_l))

            # Remove overlapping rectangles (optional for efficiency)
            self.free_rectangles = self.prune_free_rectangles()

        return poses, total_boxes

    def prune_free_rectangles(self):
        """
        Remove redundant rectangles from the free rectangle list.
        """
        pruned = []
        for rect in self.free_rectangles:
            x, y, w, l = rect
            if all(not self.is_contained(rect, other) for other in self.free_rectangles):
                pruned.append(rect)
        return pruned

    @staticmethod
    def is_contained(rect1, rect2):
        """
        Check if rect1 is fully contained in rect2.
        """
        x1, y1, w1, l1 = rect1
        x2, y2, w2, l2 = rect2
        return x1 >= x2 and y1 >= y2 and x1 + w1 <= x2 + w2 and y1 + l1 <= y2 + l2

def visualize(box, pallet, poses):
    """
    Visualize the placement of boxes on the pallet.

    Args:
        box (Box): The box dimensions.
        pallet (Pallet): The pallet dimensions.
        poses (list): List of tuples representing the poses (x, y, theta).
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, pallet.width)
    ax.set_ylim(0, pallet.length)
    ax.set_aspect('equal')
    ax.set_title("Palletizing Pattern")
    ax.set_xlabel("Width (cm)")
    ax.set_ylabel("Length (cm)")

    # Draw the pallet
    ax.add_patch(
        plt.Rectangle((0, 0), pallet.width, pallet.length, edgecolor='black', facecolor='lightgray', lw=2)
    )

    # Draw each box
    for x, y, theta in poses:
        if theta == 0:
            w, l = box.width, box.length
        else:
            w, l = box.length, box.width
        ax.add_patch(
            plt.Rectangle((x, y), w, l, edgecolor='blue', facecolor='skyblue', lw=1)
        )

    plt.show()

