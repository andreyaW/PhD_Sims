import numpy as np

class MarkovDecisionProcess:
    def __init__(self, states, actions, transition_probabilities, rewards, discount_factor):
        self.states = states
        self.actions = actions
        self.transition_probabilities = transition_probabilities
        self.rewards = rewards
        self.discount_factor = discount_factor

    def value_iteration(self, threshold=1e-6):
        value_table = np.zeros(len(self.states))
        while True:
            updated_value_table = np.copy(value_table)
            for state in range(len(self.states)):
                Q_value = []
                for action in range(len(self.actions)):
                    q_value = sum([self.transition_probabilities[state][action][next_state] * 
                                   (self.rewards[state][action][next_state] + self.discount_factor * value_table[next_state]) 
                                   for next_state in range(len(self.states))])
                    Q_value.append(q_value)
                updated_value_table[state] = max(Q_value)
            if np.sum(np.fabs(updated_value_table - value_table)) <= threshold:
                break
            value_table = updated_value_table
        return value_table

# Example usage
states = [0, 1, 2]
actions = [0, 1]
transition_probabilities = [
    [[0.7, 0.3, 0.0], [0.4, 0.6, 0.0]],
    [[0.1, 0.9, 0.0], [0.0, 0.8, 0.2]],
    [[0.0, 0.0, 1.0], [0.0, 0.0, 1.0]]
]
rewards = [
    [[5, 10, 0], [2, 4, 0]],
    [[1, 2, 0], [0, 3, 5]],
    [[0, 0, 0], [0, 0, 0]]
]
discount_factor = 0.9

mdp = MarkovDecisionProcess(states, actions, transition_probabilities, rewards, discount_factor)
optimal_values = mdp.value_iteration()
print("Optimal Values:", optimal_values)