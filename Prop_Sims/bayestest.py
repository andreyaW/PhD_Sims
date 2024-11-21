import pyAgrum as gum
import pyAgrum.lib.notebook as gnb

# Create a Bayesian Network
bn = gum.BayesNet('Example_BN')

# Add nodes
parent = bn.add("Parent_Object")
child_a = bn.add("Child_Object_A")
child_b = bn.add("Child_Object_B")

# Add arcs (dependencies)
bn.addArc(child_a, parent)
bn.addArc(child_b, parent)

# Define the conditional probability tables (CPTs)
bn.cpt(child_a).fillWith([0.7, 0.3])  # Probabilities for Child_Object_A (True, False)
bn.cpt(child_b).fillWith([0.6, 0.4])  # Probabilities for Child_Object_B (True, False)

# Probabilities for Parent_Object given Child_Object_A and Child_Object_B
bn.cpt(parent)[{'Child_Object_A': 0, 'Child_Object_B': 0}] = [0.9, 0.1]
bn.cpt(parent)[{'Child_Object_A': 0, 'Child_Object_B': 1}] = [0.8, 0.2]
bn.cpt(parent)[{'Child_Object_A': 1, 'Child_Object_B': 0}] = [0.4, 0.6]
bn.cpt(parent)[{'Child_Object_A': 1, 'Child_Object_B': 1}] = [0.2, 0.8]

# Display the Bayesian Network with its CPTs
gnb.showBN(bn)
