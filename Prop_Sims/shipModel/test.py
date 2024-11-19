import numpy as np
import random

import os

print(os.environ.get('VIRTUAL_ENV'))

# Define states for the component and sensor
component_states = ["Working", "Degraded", "Failed"]
sensor_states = ["Accurate", "Delayed", "Failed"]

# Transition matrices
# Rows represent current state; columns represent next state
component_transition = np.array([
    [0.90, 0.08, 0.02],  # Working -> (Working, Degraded, Failed)
    [0.20, 0.70, 0.10],  # Degraded -> (Working, Degraded, Failed)
    [0.00, 0.00, 1.00],  # Failed -> (Working, Degraded, Failed)
])

sensor_transition = np.array([
    [0.95, 0.04, 0.01],  # Accurate -> (Accurate, Delayed, Failed)
    [0.30, 0.60, 0.10],  # Delayed -> (Accurate, Delayed, Failed)
    [0.00, 0.00, 1.00],  # Failed -> (Accurate, Delayed, Failed)
])

# Function to simulate one step in a Markov chain
def next_state(current_state, transition_matrix):
    return np.random.choice(
        range(len(transition_matrix)),
        p=transition_matrix[current_state]
    )

# Simulation function
def simulate_markov_chain(steps=100):
    # Initialize states
    component_state = 0  # Start at "Working"
    sensor_state = 0     # Start at "Accurate"
    
    history = []
    
    for _ in range(steps):
        # Store current state
        history.append((component_states[component_state], sensor_states[sensor_state]))
        
        # Update states
        component_state = next_state(component_state, component_transition)
        sensor_state = next_state(sensor_state, sensor_transition)
    
    return history

# Run simulation
simulation_steps = 50
results = simulate_markov_chain(steps=simulation_steps)

# Print results
print(f"{'Step':<5} {'Component State':<10} {'Sensor State':<10}")
for step, (component, sensor) in enumerate(results, 1):
    print(f"{step:<5} {component:<15} {sensor:<15}")