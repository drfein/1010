# 2x2-block L in all four orientations
L_2x2_1 = (
    (1, 1),
    (1, 0)
)

L_2x2_2 = (
    (1, 1),
    (0, 1)
)

L_2x2_3 = (
    (0, 1),
    (1, 1)
)

L_2x2_4 = (
    (1, 0),
    (1, 1)
)

# 2x2 square
SQUARE_2x2 = (
    (1, 1),
    (1, 1)
)

# 3x3 square
SQUARE_3x3 = (
    (1, 1, 1),
    (1, 1, 1),
    (1, 1, 1)
)

# 3x3 L shape in all four orientations
L_3x3_1 = (
    (1, 1, 1),
    (1, 0, 0),
    (1, 0, 0)
)

L_3x3_2 = (
    (1, 1, 1),
    (0, 0, 1),
    (0, 0, 1)
)

L_3x3_3 = (
    (1, 0, 0),
    (1, 0, 0),
    (1, 1, 1)
)

L_3x3_4 = (
    (0, 0, 1),
    (0, 0, 1),
    (1, 1, 1)
)

# 1 single block
SINGLE_BLOCK = (
    (1,),
)

# Blocks in a row
TWO_HORIZONTAL = ((1, 1),)
TWO_VERTICAL = (
    (1,),
    (1,)
)

THREE_HORIZONTAL = ((1, 1, 1),)
THREE_VERTICAL = (
    (1,),
    (1,),
    (1,)
)

FOUR_HORIZONTAL = ((1, 1, 1, 1),)
FOUR_VERTICAL = (
    (1,),
    (1,),
    (1,),
    (1,)
)

FIVE_HORIZONTAL = ((1, 1, 1, 1, 1),)
FIVE_VERTICAL = (
    (1,),
    (1,),
    (1,),
    (1,),
    (1,)
)

# List of all shapes for easy access in your game
ALL_SHAPES = [L_2x2_1, L_2x2_2, L_2x2_3, L_2x2_4, SQUARE_2x2, SQUARE_3x3, L_3x3_1, L_3x3_2, L_3x3_3, L_3x3_4, 
              SINGLE_BLOCK, TWO_HORIZONTAL, TWO_VERTICAL, THREE_HORIZONTAL, THREE_VERTICAL, FOUR_HORIZONTAL, 
              FOUR_VERTICAL, FIVE_HORIZONTAL, FIVE_VERTICAL]

SHAPE_COLORS = {
    L_2x2_1: 1,
    L_2x2_2: 2,
    L_2x2_3: 3,
    L_2x2_4: 4,
    SQUARE_2x2: 5,
    SQUARE_3x3: 6,
    L_3x3_1: 7,
    L_3x3_2: 8,
    L_3x3_3: 9,
    L_3x3_4: 10,
    SINGLE_BLOCK: 11,
    TWO_HORIZONTAL: 12,
    TWO_VERTICAL: 13,
    THREE_HORIZONTAL: 14,
    THREE_VERTICAL: 15,
    FOUR_HORIZONTAL: 16,
    FOUR_VERTICAL: 17,
    FIVE_HORIZONTAL: 18,
    FIVE_VERTICAL: 19
}
COLOR_KEY = {
    1: (237, 41, 57),   # Soft Red
    2: (102, 204, 0),   # Bright Green
    3: (0, 128, 255),   # Sky Blue
    4: (255, 203, 5),   # Golden Yellow
    5: (153, 51, 255),  # Lavender Purple
    6: (0, 204, 204),   # Turquoise Cyan
    7: (204, 0, 0),     # Rich Dark Red
    8: (0, 153, 0),     # Forest Green
    9: (0, 51, 102),    # Deep Blue
    10: (204, 204, 0),  # Olive Yellow
    11: (102, 0, 102),  # Plum Purple
    12: (0, 102, 102),  # Teal
    13: (160, 160, 160),# Soft Gray
    14: (153, 0, 0),    # Maroon Red
    15: (0, 102, 0),    # Dark Leaf Green
    16: (0, 0, 153),    # Navy Blue
    17: (128, 128, 0),  # Mustard Yellow
    18: (102, 0, 0),    # Burgundy Red
    19: (0, 51, 0),     # Dark Green
}
