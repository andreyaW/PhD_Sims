import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Create a figure and axes
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Create a ship object
ship, = ax.plot([], [], 'bo')

# Function to update the ship's position
def update(frame):
    x = frame % 10
    y = 5
    ship.set_data(x, y)
    return ship,

# Create the animation
ani = FuncAnimation(fig, update, frames=range(100), interval=100, blit=True)

# Show the animation
plt.show()