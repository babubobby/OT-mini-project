import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

G = nx.complete_graph(10)  # 10 nodes (intersections)
positions = nx.spring_layout(G, seed=42)  # Layout for visualization

for (u, v) in G.edges():
    G.edges[u, v]['weight'] = random.randint(5, 25)

alpha = 1.0         
beta = 2.0           
evaporation = 0.5    
Q = 100              
num_ants = 10
num_iterations = 100

pheromone = np.ones((len(G.nodes), len(G.nodes)))

def distance(u, v):
    return G.edges[u, v]['weight']

def probability(pheromone, u, v, visited):
    if v in visited:
        return 0
    return (pheromone[u][v] ** alpha) * ((1.0 / distance(u, v)) ** beta)

def choose_next_node(pheromone, current, visited):
    probs = [probability(pheromone, current, j, visited) for j in G.nodes]
    total = sum(probs)
    if total == 0:
        return random.choice([j for j in G.nodes if j not in visited])
    probs = [p / total for p in probs]
    return np.random.choice(list(G.nodes), p=probs)

def ant_colony_optimization(start, end):
    best_path = None
    best_length = float('inf')
    convergence = []

    global pheromone

    for iteration in range(num_iterations):
        all_paths = []
        all_lengths = []

        for _ in range(num_ants):
            path = [start]
            visited = set(path)
            current = start

            while current != end:
                next_node = choose_next_node(pheromone, current, visited)
                path.append(next_node)
                visited.add(next_node)
                current = next_node
                if len(visited) == len(G.nodes):
                    break

            path_length = sum(distance(path[i], path[i+1]) for i in range(len(path)-1))
            all_paths.append(path)
            all_lengths.append(path_length)

            if path[-1] == end and path_length < best_length:
                best_path = path
                best_length = path_length

        pheromone *= (1 - evaporation)
        for path, length in zip(all_paths, all_lengths):
            for i in range(len(path) - 1):
                pheromone[path[i]][path[i+1]] += Q / length

        convergence.append(best_length)

    return best_path, best_length, convergence

start_node = 0
end_node = 9
best_path, best_length, convergence = ant_colony_optimization(start_node, end_node)

print("Best Path:", best_path)
print("Path Length:", best_length)

plt.figure(figsize=(12, 6))

plt.subplot(121)
nx.draw(G, positions, with_labels=True, node_color='skyblue', node_size=700)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, positions, edge_labels=edge_labels)
nx.draw_networkx_edges(G, positions, edgelist=list(zip(best_path, best_path[1:])), edge_color='r', width=2)
plt.title("Best Route Found Using ACO")

plt.subplot(122)
plt.plot(convergence, color='green')
plt.xlabel("Iteration")
plt.ylabel("Path Length")
plt.title("ACO Convergence")

plt.tight_layout()
plt.show()
