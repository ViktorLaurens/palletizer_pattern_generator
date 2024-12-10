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

    def place_greedy(self, box):
        """
        Place boxes on the pallet using a greedy search.

        Args:
            box (Box): The box to place.

        Returns:
            list: List of tuples representing the poses (x, y, theta).
            int: Total number of boxes placed.
        """
        patterns_to_check = []
        explored_patterns = []
        max_boxes = self.calculate_upper_bound(box)
        if max_boxes == 0:
            return [], 0

        # Initialize patterns with boxes without rotation and boxes with rotation
        # Without rotation
        n_boxes_w = self.width // box.width
        n_boxes_l = self.length // box.length
        n_boxes = int(n_boxes_w * n_boxes_l)
        pattern = [(i * box.width, j * box.length, 0) for i in range(n_boxes_w) for j in range(n_boxes_l)]
        usable_space = self.calc_usable_space(pattern, box)
        patterns_to_check.append((n_boxes, usable_space, pattern))
        if n_boxes == max_boxes:
            return pattern, max_boxes
        
        # With rotation
        n_boxes_w = self.width // box.length
        n_boxes_l = self.length // box.width
        n_boxes = int(n_boxes_w * n_boxes_l)
        pattern = [(i * box.length, j * box.width, 90) for i in range(n_boxes_w) for j in range(n_boxes_l)]
        usable_space = self.calc_usable_space(pattern, box)
        patterns_to_check.append((n_boxes, usable_space, pattern))
        if n_boxes == max_boxes:
            return pattern, max_boxes

        while patterns_to_check:
            # Take the pattern with the most usable space
            n_boxes, usable_space, pattern = max(patterns_to_check, key=lambda x: x[1])
            patterns_to_check.remove((n_boxes, usable_space, pattern))

            # Check for free space
            free_space_rectangles = self.calc_free_space_rectangles(pattern, box)
            # For each free rectangle, check if boxes can be placed
            usable_rectangles = [
                rect for rect in free_space_rectangles if self.check_free_space_rectangle(rect, box)
            ]
            if not usable_rectangles:
                # No more boxes can be placed
                explored_patterns.append((n_boxes, usable_space, pattern))
                continue    
            else:
                # Choose biggest usable rectangle to fill
                rect_to_fill = max(usable_rectangles, key=lambda r: r[2] * r[3])
                # Fill the free space with boxes both with and without rotation and add to patterns_to_check
                x, y, w, l = rect_to_fill
                
                # Without rotation
                n_boxes_w = w // box.width
                n_boxes_l = l // box.length
                n_boxes_rect_1 = int(n_boxes_w * n_boxes_l)
                pattern_rect_1 = [
                    (x + i * box.width, y + j * box.length, 0)
                    for i in range(n_boxes_w)
                    for j in range(n_boxes_l)
                ]
                usable_space = self.calc_usable_space(pattern + pattern_rect_1, box)
                patterns_to_check.append((n_boxes + n_boxes_rect_1, usable_space, pattern + pattern_rect_1))
                if n_boxes + n_boxes_rect_1 == max_boxes:
                    return pattern + pattern_rect_1, max_boxes
                
                # With rotation
                n_boxes_w = w // box.length
                n_boxes_l = l // box.width
                n_boxes_rect_2 = int(n_boxes_w * n_boxes_l)
                pattern_rect_2 = [
                    (x + i * box.length, y + j * box.width, 90)
                    for i in range(n_boxes_w)
                    for j in range(n_boxes_l)
                ]
                usable_space = self.calc_usable_space(pattern + pattern_rect_2, box)
                patterns_to_check.append((n_boxes + n_boxes_rect_2, usable_space, pattern + pattern_rect_2))
                if n_boxes + n_boxes_rect_2 == max_boxes:
                    return pattern + pattern_rect_2, max_boxes
                
                # Add the better pattern to patterns_to_check
                if n_boxes_rect_1 >= n_boxes_rect_2:
                    patterns_to_check.append((n_boxes + n_boxes_rect_1, usable_space, pattern + pattern_rect_1))
                else:
                    patterns_to_check.append((n_boxes + n_boxes_rect_2, usable_space, pattern + pattern_rect_2))

        # Return the best pattern
        best_pattern = max(explored_patterns, key=lambda x: x[0])
        return best_pattern[2], best_pattern[0]
    
    def calculate_upper_bound(self, box):
        """Calculate the upper bound for the number of boxes that can fit on the pallet."""
        pallet_area = self.width * self.length
        box_area = box.width * box.length
        return pallet_area // box_area

    def calc_usable_space(self, pattern, box):
        """Calculate the usable space for a given pattern. This includes both the space that is already taken in by boxes as well as the space that can still be taken in by boxes."""
        area_box = box.width * box.length
        amount_boxes = len(pattern)
        used_space = amount_boxes * area_box
        usable_space = used_space
        free_space_rectangles = self.calc_free_space_rectangles(pattern, box)
        for rect in free_space_rectangles:
            _, _, w, l = rect
            if self.check_free_space_rectangle(rect, box):
                usable_space += w * l
        return usable_space
    
    def calc_free_space_rectangles(self, pattern, box):
        """
        Calculate two large rectangles representing the free space in the pallet.

        Args:
            pallet (Pallet): The pallet dimensions (width, length).
            pattern (list): A list of placed boxes, each as (x, y, theta).

        Returns:
            list: Two rectangles (above and right), as (x, y, width, length).
        """
        # Step 1: Determine the covered area
        if not pattern:
            return []
        max_x = max(x + (box.width if theta == 0 else box.length) for x, y, theta in pattern)
        max_y = max(y + (box.length if theta == 0 else box.width) for x, y, theta in pattern)

        # Step 2: Calculate the remaining rectangles
        rectangles = []

        # Rectangle above the covered area
        above_rect = (0, max_y, self.width, self.length - max_y)
        rectangles.append(above_rect)

        # Rectangle to the right of the covered area
        right_rect = (max_x, 0, self.width - max_x, self.length)
        rectangles.append(right_rect)
        return rectangles

    def check_free_space_rectangle(self, rect, box):
        """
        Check if a box can fit in a free space rectangle.

        Args:
            rect (tuple): A rectangle as (x, y, width, length).
            box (Box): The box dimensions.

        Returns:
            bool: True if the box can fit, False otherwise.
        """
        _, _, rect_width, rect_length = rect

        # Check if the box fits in either orientation
        return (box.width <= rect_width and box.length <= rect_length) or \
            (box.length <= rect_width and box.width <= rect_length)

def visualize(box, pallet, pattern, title="Palletizing Pattern"):
    """
    Visualize the placement of boxes on the pallet.

    Args:
        box (Box): The box dimensions.
        pallet (Pallet): The pallet dimensions.
        pattern (list): List of tuples representing the poses (x, y, theta).
        title (str): Title of the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, pallet.width)
    ax.set_ylim(0, pallet.length)
    ax.set_aspect('equal')
    ax.set_title(title)  # Use the dynamic title here
    ax.set_xlabel("Width (cm)")
    ax.set_ylabel("Length (cm)")

    # Draw the pallet
    ax.add_patch(
        plt.Rectangle((0, 0), pallet.width, pallet.length, edgecolor='black', facecolor='lightgray', lw=2)
    )

    # Draw each box
    for x, y, theta in pattern:
        if theta == 0:
            w, l = box.width, box.length
        else:
            w, l = box.length, box.width
        ax.add_patch(
            plt.Rectangle((x, y), w, l, edgecolor='blue', facecolor='skyblue', lw=1)
        )

    plt.show()

def visualize_multiple(pallet, box_patterns, title="Palletizing Pattern"):
    """
    Visualize the placement of multiple box types on the pallet.

    Args:
        pallet (Pallet): The pallet dimensions.
        box_patterns (list): A list of tuples (Box, pattern, color), where:
                             - Box: The box dimensions.
                             - pattern: List of tuples representing the poses (x, y, theta).
                             - color: The color to use for the boxes of this type.
        title (str): Title of the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, pallet.width)
    ax.set_ylim(0, pallet.length)
    ax.set_aspect('equal')
    ax.set_title(title)
    ax.set_xlabel("Width (cm)")
    ax.set_ylabel("Length (cm)")

    # Draw the pallet
    ax.add_patch(
        plt.Rectangle((0, 0), pallet.width, pallet.length, edgecolor='black', facecolor='lightgray', lw=2)
    )

    # Draw each box type
    for box, pattern, color in box_patterns:
        for x, y, theta in pattern:
            if theta == 0:
                w, l = box.width, box.length
            else:
                w, l = box.length, box.width
            ax.add_patch(
                plt.Rectangle((x, y), w, l, edgecolor=color, facecolor=color, alpha=0.5, lw=1)
            )

    # Add a legend
    handles = [plt.Rectangle((0, 0), 1, 1, color=color, alpha=0.5) for _, _, color in box_patterns]
    labels = [f"Box ({box.width}x{box.length} cm)" for box, _, _ in box_patterns]
    ax.legend(handles, labels, loc='upper right')

    plt.show()
