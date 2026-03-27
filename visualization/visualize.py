import matplotlib.pyplot as plt
import numpy as np

# Parameters
grid_size = (10, 10)  # Size of the grid
obstacles = [(3, 3), (3, 4), (4, 4), (5, 5)]  # List of obstacles
items = [(0, 1), (1, 0), (8, 8)]  # List of items
path = [(0, 0), (1, 1), (2, 2), (3, 3)]  # Example path

# Delivery point
delivery_point = (9, 9)

# Create a grid
grid = np.zeros(grid_size)

# Mark obstacles
for obs in obstacles:
    grid[obs] = 1  # Mark obstacle with 1

# Plotting
plt.figure(figsize=(8, 8))
plt.imshow(grid, origin='lower', cmap='Greys', alpha=0.6)

# Plot path
path_x, path_y = zip(*path)
plt.plot(path_x, path_y, marker='o', color='blue', label='Path')

# Plot items
item_x, item_y = zip(*items)
plt.scatter(item_x, item_y, color='green', s=100, label='Items')

# Plot delivery point
plt.scatter(*delivery_point, color='red', s=200, label='Delivery Point')

# Add additional elements
plt.title('Warehouse Robot Visualization')
plt.xlim(-0.5, grid_size[0]-0.5)
plt.ylim(-0.5, grid_size[1]-0.5)
plt.xticks(range(grid_size[0]))
plt.yticks(range(grid_size[1]))
plt.grid(True)
plt.gca().invert_yaxis()  # Invert y-axis to match grid coordinates
plt.legend()
plt.show()