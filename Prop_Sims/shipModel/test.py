import matplotlib.pyplot as plt
import numpy as np

# Define the states and transition probabilities
states = ["Sunny", "Cloudy", "Rainy"]
transition_matrix = np.array([[0.6, 0.3, 0.1],
                               [0.2, 0.5, 0.3],
                               [0.1, 0.4, 0.5]])

# Create a figure and axes
fig, ax = plt.subplots()

# Draw the states as nodes
for i, state in enumerate(states):
    ax.add_patch(plt.Circle((i, 0), radius=0.1, color="white", ec="black"))
    ax.text(i, 0, state, ha="center", va="center", fontsize=12)

# Draw the transitions as arrows
for i, row in enumerate(transition_matrix):
    for j, prob in enumerate(row):
        if prob > 0:
            ax.annotate("", xy=(j, 0), xytext=(i, 0),
                        arrowprops=dict(arrowstyle="-|>", color="black", lw=prob*2))
            ax.text((i+j)/2, 0.1, f"{prob:.2f}", ha="center", va="center", fontsize=10)

# Set the axis limits and labels
ax.set_xlim(-0.5, len(states)-0.5)
ax.set_ylim(-0.5, 0.5)
ax.set_yticks([])

# Show the plot
plt.show()




# # Print results
# print(f"{'Step':<5} {'Component State':<10} {'Sensor State':<10}")
# for step, (component, sensor) in enumerate(results, 1):
#     print(f"{step:<5} {component:<15} {sensor:<15}")