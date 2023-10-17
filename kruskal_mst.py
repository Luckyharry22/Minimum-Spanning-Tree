# Name: Harmeet Singh
# Kruskal's algorithm


import time

# ---------------------------------------------------- #
### Implementing priority queue using linked list
# ---------------------------------------------------- #
# Defining a node class
class Node:
    def __init__(self, data, priority):
        self.data = data
        self.priority = priority
        self.next = None

# ---------------------------------------------------- #
# Defining the Priority Queue class using Node class
# ---------------------------------------------------- #
class Priority_queue:
    # Initializing an empty priority queue
    def __init__(self):
        self.head = None
    
    # Utility function to check if PQ is empty
    def isEmpty(self):
        return self.head == None
    
    # Utility function to insert an element to PQ
    def push(self, val, priority):
        if self.isEmpty():
            self.head = Node(val, priority)
            return 1
        else:
            if self.head.priority > priority:
                temp = Node(val, priority)
                temp.next = self.head
                self.head = temp
                return 1
            else:
                temp = self.head
                while temp.next != None and temp.next.priority < priority:
                    temp = temp.next
                new_node = Node(val, priority)
                new_node.next = temp.next
                temp.next = new_node
                return 1
    
    # Utility function to delete the element with highest priority
    def delete_min(self):
        if self.isEmpty():
            return 0
        else:
            self.head = self.head.next
            return 1
    
    # Utility function to return the element with highest priority
    def top(self): 
        if self.isEmpty():
            return -1
        else:
            return self.head.data


# ---------------------------------------------------- #
### Implementing MFSET (also known as Disjoint Set)
# ---------------------------------------------------- #
# I will be using the faster implementation of MFSET 
# using tree and path compression (sec.: 5.5 of AHU book)
# ---------------------------------------------------- #
class Mfset:
    #Initializing the MFSET for n elements
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0 for i in range(n)]

    # Utility function to find the parent of an element
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    # Utility function to merge two sets based on the rank of the sets(for path compression)
    def merge(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self.rank[a] > self.rank[b]:
            self.parent[b] = a
        else:
            self.parent[a] = b
            if self.rank[a] == self.rank[b]:
                self.rank[b] += 1

# ---------------------------------------------------- #
### Implementing Graph class
# ---------------------------------------------------- #
# I will be using the edge list representation
# where the list will store edges in the form of tuples
# (u, v, weight)
# ---------------------------------------------------- #
class Graph:
    # Initializing an empty graph with n vertices
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = []

    # Utility function to get the number of vertices in the graph
    def length(self):
        return self.vertices
    
    # Utility function to add an edge to the graph
    def add_edge(self, u, v, weight):
        self.graph.append((u, v, weight))

    # Utility function to print the graph
    def printWithWeights(self):
        for u,v,w in self.graph:
            print(f"({u+1},{v+1},{w})")
    
    # Utility function to print the graph without weights
    def printWithoutWeights(self):
        for u,v,w in self.graph:
            print(f"({u+1},{v+1})")

    # Utility function to store and get total weight of the graph (for MST)
    def setTotalWeight(self, weight):
        self.total_weight = weight
    def getTotalWeight(self):
        return self.total_weight

# ---------------------------------------------------- #
### Implementing Kruskal's algorithm
# ---------------------------------------------------- #
def KruskalMST(g):
    MSTset = []

    # Defining some utility variables
    i,edge_count = [0,0]

    # Sorting the edges in ascending order of their weights
    g.graph = sorted(g.graph, key=lambda item: item[2])

    # Initializing the MFSET
    mfset = Mfset(g.length())

    # Looping until we have V-1 edges in the MST
    while edge_count < g.length() - 1:
        # Extracting the edge with minimum weight
        u,v,w = g.graph[i]
        i += 1
        a = mfset.find(u)
        b = mfset.find(v)

        # Checking if the edge is creating a cycle or not
        # If it isn't creating a cycle, add it to the MST
        if a != b:
            edge_count += 1
            MSTset.append((u,v,w))
            mfset.merge(a, b)
    
    # Calculating the total weight of the MST
    total_weight = 0
    for u,v,w in MSTset:
        total_weight += w
    
    # Create a new empty graph with n nodes
    MST = Graph(g.length())
    # Add the edges of the MST to the new graph
    for u,v,w in MSTset:
        MST.add_edge(u, v, w)
    # Set the total weight of the MST
    MST.setTotalWeight(total_weight)

    return MST


# Driver class
if __name__=="__main__":
    # Initializing the start time
    start = time.time()

    # Taking input from file
    inp = open("input.txt", "r")
    n = int(inp.readline().split()[0])
    matrix = [[int(i) for i in line.split()] for line in inp.readlines()]

    # We got the graph in matrix form (according to input specified in the assignment)
    # We will convert it into edge list form
    edge_list = []
    for i in range(n):
        for j in range(i+1, n):
            if matrix[i][j] > 0:
                edge_list.append((i, j, matrix[i][j]))

    # Creating a graph object
    g = Graph(vertices = n)
    # Adding the edges to the graph object
    for u,v,w in edge_list:
        g.add_edge(u, v, w)
    

    # Calling Kruskal's algorithm
    MST = KruskalMST(g)


    # Initializing the end time
    end = time.time()
    # Calculating runtime
    runtime = round((end - start) * 1000, 2)

    # Printing the edges of the MST
    print(f"Kruskal's algorithm MST (total cost: {MST.getTotalWeight()}; runtime: {runtime}ms)")
    MST.printWithoutWeights()