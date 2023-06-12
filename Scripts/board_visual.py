import random
import string
from collections import defaultdict
import matplotlib.colors as mcolors
import numpy as np
import matplotlib.pyplot as plt


# maak gwn lijst met kleuren. 

def generate_random_color():
    """
    Generate a random color in hexadecimal format.
    """
    color = ''.join(random.choices(string.hexdigits[:-6], k=6))
    return '#' + color


def colorize_string_list(string_list):
    """
    Color each character in the string list with a random color.
    '_' characters are colored white
    'X' characters are colored red
    """
    color_map = defaultdict(generate_random_color)
    color_map['_'] = '#FFFFFF'  # Set the color for '_' to white
    color_map['X'] = '#FF0000'
    colorized_string_list = [color_map[char] for char in string_list]
    return colorized_string_list


def create_color_matrix(data):
    """
    Create an empty matrix to hold the color.
    """
    x_coords = []
    y_coords = []
    colors = [] 

    for coord, color in data.items():
        y_coords.append(coord[0])
        x_coords.append(coord[1])
        colors.append(color)

    colored_string_list = colorize_string_list(colors)

    # Create a grid of coordinates
    x_coords = sorted(set(x_coords))
    y_coords = sorted(set(y_coords))

    # Convert color strings to RGB values
    rgb_values = [mcolors.hex2color(color) for color in colored_string_list]

    # Create an empty matrix to hold the color
    color_matrix = np.empty((len(y_coords), len(x_coords), 3), dtype='float')

    # Fill the matrix with the RGB values
    for coord, rgb_value in zip(data.keys(), rgb_values):
        x = coord[1]
        y = coord[0]
        x_index = x_coords.index(x)
        y_index = y_coords.index(y)
        color_matrix[y_index, x_index] = rgb_value

    # Plot the color matrix using imshow
    fig, ax = plt.subplots(facecolor='black')
    ax.imshow(color_matrix)

    ax.axis('off')

    # Display the plot
    plt.show()


if __name__ == '__main__':
        
    data = {(1, 1): '_', (1, 2): 'A', (1, 3): 'A', (1, 4): 'B', (1, 5): 'B', (1, 6): 'B',
            (2, 1): '_', (2, 2): 'C', (2, 3): 'C', (2, 4): 'E', (2, 5): 'D', (2, 6): 'D',
            (3, 1): 'X', (3, 2): 'X', (3, 3): 'G', (3, 4): 'E', (3, 5): '_', (3, 6): 'I',
            (4, 1): 'F', (4, 2): 'F', (4, 3): 'G', (4, 4): 'H', (4, 5): 'H', (4, 6): 'I',
            (5, 1): 'K', (5, 2): '_', (5, 3): 'L', (5, 4): '_', (5, 5): 'J', (5, 6): 'J',
            (6, 1): 'K', (6, 2): '_', (6, 3): 'L', (6, 4): '_', (6, 5): '_', (6, 6): '_'}

    create_color_matrix(data)
