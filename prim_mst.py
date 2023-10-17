# Name: Harmeet Singh
# Prim's algorithm


import time


# ---------------------------------------------------- #
### Implementing Graph class
# ---------------------------------------------------- #
# I willbe implementing the graph using adjacency matrix
# ---------------------------------------------------- #
class Graph:
    # General functions

    # Initializing the graph
    def __init__(self, vertices = 0, matrix = None, input_graph = None, parent = None):
        if input_graph != None and parent != None:
            self.createMSTgraph(vertices, input_graph, parent)
        else:
            self.vertices = vertices
            self.graph = matrix

    # Get the number of vertices in the graph
    def length(self):
        return self.vertices
    
    # Add an edge to the graph
    def add_edge(self, u, v, weight):
        u = int(u) - 1
        v = int(v) - 1
        weight = int(weight)
        self.graph[u][v] = self.graph[v][u] = weight

    # Print the graph
    def print(self):
        for row in self.graph:
            for col in row:
                print(col, end=" ")
            print()


    # Utility functions for Prim's algorithm
    
    # 1. Find the vertex with the minimum cost which is not already included in the MST
    def minKey(self, lowest_cost_to_vertex, MSTset):
        min_vertex_cost = float('inf')
        min_vertex = -1

        for v in range(self.vertices):
            if lowest_cost_to_vertex[v] < min_vertex_cost and MSTset[v] == False:
                min_vertex_cost = lowest_cost_to_vertex[v]
                min_vertex = v
        return min_vertex
    
    # 2. Create a MST using the parent array
    def createMSTgraph(self, vertices, input_graph, parent):
        # Set the number of vertices and create an empty graph
        self.vertices = vertices
        self.graph = [ [0 for i in range(vertices)] for i in range(vertices) ]

        # Set the edges present in MST to have weight of 1 (we will use this as a mask o the previous graph)
        for i in range(len(parent)):
            u = i
            v = parent[i]
            if v == -1:
                continue
            self.graph[u][v] = self.graph[v][u] = 1
        
        # Set the edges of the MST to have the same weight as the original graph (only the edges that are included in the MST)
        for i in range(vertices):
            for j in range(vertices):
                if self.graph[i][j] > 0:
                    self.graph[i][j] = self.graph[j][i] = input_graph[i][j]

    # 3. Print edges of the Graph (for ouput according to the assignment)
    def print_edges(self):
        for i in range(self.vertices):
            for j in range(i+1, self.vertices):
                if self.graph[i][j] != 0:
                    print(f"({i+1},{j+1})")
    
    # 4. Get total weight of the edges of graph (for MST)
    def getTotalWeight(self):
        total_weight = 0
        for i in range(self.vertices):
            for j in range(i+1, self.vertices):
                if self.graph[i][j] != 0:
                    total_weight += self.graph[i][j]
        return total_weight

# ---------------------------------------------------- #
# Prim's algorithm 
# ---------------------------------------------------- #
# (taking graph as input and outputting MST in graph form)
# ---------------------------------------------------- #
def prim(g):
    n = g.length()

    # Initialize lists for storing the lowest cost to vertex and closest vertex of each vertex
    lowest_cost_to_vertex = [float('inf')] * n
    closest = [None] * n 

    # Create a set to keep track of vertices already included in MST
    MSTset = [False] * n

    # Start from vertex 0 (set minimum cost to vertex as zero)
    lowest_cost_to_vertex[0] = 0
    
    # Set closest of that vertex as -1 (Because it is the starting vertex of tree)
    closest[0] = -1

    # Looping to add n-1 edges to the MST
    for cnt in range(n-1):
        # Find the vertex u outside of the set U with the minimum lowcost
        u = g.minKey(lowest_cost_to_vertex, MSTset)
        MSTset[u] = True

        #Update the Lowest cost to vertex and closest arrays after including the current taken vertex
        for j in range(n):
            # If vertex j is not in MST and there exists an edge from u to j
            # and the cost of that edge is less than the previous lowest cost to j
            # Update lowest cost to j and closest of j
            if g.graph[u][j] > 0 and MSTset[j] == False and lowest_cost_to_vertex[j] > g.graph[u][j]:
                lowest_cost_to_vertex[j] = g.graph[u][j]
                closest[j] = u

    # Create a MST using Graph class
    MST = Graph(vertices = n, input_graph = g.graph, parent = closest)
    
    return MST

if __name__ == "__main__":
    # Initializing the start time
    start = time.time()

    # Taking input from file
    inp = open("input.txt", "r")
    n = int(inp.readline().split()[0])
    matrix = [[int(i) for i in line.split()] for line in inp.readlines()]
    g = Graph(vertices = n, matrix = matrix)

    # Calling Prim's algorithm
    MST = prim(g)

    # Initializing the end time
    end = time.time()

    # Calculating runtime
    runtime = round((end - start) * 1000, 2)

    # Printing the results
    print(f"Prim's algorithm MST (total cost: {MST.getTotalWeight()}; runtime: {runtime}ms)")
    MST.print_edges()

