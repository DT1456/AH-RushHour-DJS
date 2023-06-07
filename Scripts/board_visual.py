import random
import string
from collections import defaultdict
import matplotlib.colors as mcolors
import numpy as np

def generate_random_color():
    """
    Generate a random color in hexadecimal format.
    """
    color = ''.join(random.choices(string.hexdigits[:-6], k=6))
    return '#' + color

def colorize_string_list(string_list):
    """
    colour each char in the string list with a random color.
    """
    color_map = defaultdict(generate_random_color)
    colorized_string_list = [color_map[char] for char in string_list]
    return colorized_string_list

data = {(1, 1): '_', (1, 2): 'A', (1, 3): 'A', (1, 4): 'B', (1, 5): 'B', (1, 6): 'B',
        (2, 1): '_', (2, 2): 'C', (2, 3): 'C', (2, 4): 'E', (2, 5): 'D', (2, 6): 'D',
        (3, 1): 'X', (3, 2): 'X', (3, 3): 'G', (3, 4): 'E', (3, 5): '_', (3, 6): 'I',
        (4, 1): 'F', (4, 2): 'F', (4, 3): 'G', (4, 4): 'H', (4, 5): 'H', (4, 6): 'I',
        (5, 1): 'K', (5, 2): '_', (5, 3): 'L', (5, 4): '_', (5, 5): 'J', (5, 6): 'J',
        (6, 1): 'K', (6, 2): '_', (6, 3): 'L', (6, 4): '_', (6, 5): '_', (6, 6): '_'}

x_coords = []
y_coords = []
colors = [] 

for coord, color in data.items():
    y_coords.append(coord[0])
    x_coords.append(coord[1])
    colors.append(color)

colored_string_list = colorize_string_list(colors)

# Convert color strings to RGB values
rgb_values = [mcolors.hex2color(color) for color in colored_string_list]

# Print to check if the colours work
print(rgb_values)



# Create an empty matrix to hold the colors
color_matrix = np.empty((len(y_coords), len(x_coords), 3), dtype='float')




