import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_markov_chain(num_states):
    fig, ax = plt.subplots(figsize=(num_states * 1.5, 3))
    
    # Coordinates for states
    x_coords = np.linspace(1, num_states, num_states)
    y_coord = 1

    # Draw states as circles
    state_radius = 0.2
    for i, x in enumerate(x_coords):
        # Circle for each state
        circle = plt.Circle((x, y_coord), state_radius, color='skyblue', ec='black', zorder=2)
        ax.add_patch(circle)
        # State label
        ax.text(x, y_coord, f"S{i+1}", ha='center', va='center', fontsize=12, zorder=3)

        # Recurrent arrow (loop)
        arrow = patches.FancyArrowPatch(
            (x + state_radius / 2, y_coord + state_radius / 2),
            (x - state_radius / 2, y_coord + state_radius / 2),
            connectionstyle="arc3,rad=1",
            color='black',
            arrowstyle="->",
            mutation_scale=10,
            lw=1,
        )
        ax.add_patch(arrow)

    # Draw arrows between states
    for i in range(num_states - 1):
        arrow = patches.FancyArrowPatch(
            (x_coords[i] + state_radius, y_coord),
            (x_coords[i + 1] - state_radius, y_coord),
            color='black',
            arrowstyle="->",
            mutation_scale=10,
            lw=1,
        )
        ax.add_patch(arrow)

    # Setting limits and aspect
    ax.set_xlim(0, num_states + 1)
    ax.set_ylim(0, 2)
    ax.set_aspect('equal', adjustable='datalim')
    ax.axis('off')

    plt.show()

# Example: Draw a Markov chain with 5 states
draw_markov_chain(5)
