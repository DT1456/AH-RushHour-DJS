from game import Game
# import matplotlib
# matplotlib.use('WXAgg')
import matplotlib.pyplot as plt

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

for i in range(len(colors)):
    if colors[i] == 'X':
        colors[i] = 'red'
    else:
        colors[i] = 'blue'


# Creating the scatter plot
plt.scatter(x_coords, y_coords, c=colors)

plt.show()