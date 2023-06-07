import random
import string
from collections import defaultdict

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

print(colored_string_list)



"""
#print(colors)

for i in range(len(colors)):
    if colors[i] == 'X':
        colors[i] = 'red'
    else:
        colors[i] = 'blue'



# Create an empty matrix to store the colors
matrix = np.empty((max(y_coords), max(x_coords)))

# Assign numerical values to the colors based on the coordinates
for x, y, color in zip(x_coords, y_coords, colors):
    matrix[y-1, x-1] = 0 if color == 'blue' else 1

# Display the matrix using imshow
plt.imshow(matrix, cmap='bwr')
plt.axis('off')  # Remove axis ticks
plt.show()

"""
"""
# Creating the scatter plot
plt.scatter(x_coords, y_coords, c=colors, marker= 's', s = 1000)


# Invert the y axsis to run from 6 to 1 instead of from 1 to 6
plt.gca().invert_yaxis()

# Remove axsis and tickers and boarder
plt.axis('off')



plt.show()
"""