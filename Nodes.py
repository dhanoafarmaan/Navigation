# The keys ('A', 'B', etc.) represent the nodes.
# The inner dictionaries represent outgoing connections and their weights.
import random

num_nodes = 100   # Change this to any number

graph = {}

for i in range(num_nodes):
    node = f"A{i}"
    graph[node] = {}

    if i + 1 < num_nodes:
        graph[node][f"A{i+1}"] = random.randint(1, 20)
    if i + 2 < num_nodes:
        graph[node][f"A{i+2}"] = random.randint(1, 20)
    if i + 3 < num_nodes:
        graph[node][f"A{i+3}"] = random.randint(1, 20)