import collections
import heapq
def bfs(heuristic,graph,start,goal):
    queue=([(heuristic[start],start,[start])])
    visited=[start]
    while queue:
        h,current,path=heapq.heappop(queue)
        if current==goal:
            return path,visited
        for neighbor in (graph.get(current,[])):
            if neighbor not in visited:
                visited.append(neighbor)
                npath=path+[neighbor]
                heapq.heappush(queue,(heuristic[neighbor],neighbor,npath))
    return None
graph=collections.defaultdict(dict)
num_nodes = int(input("Enter the number of nodes with heuristics: "))
print("Enter each node and its heuristic value (e.g., 'A 10')")
heuristics={}
for i in range(num_nodes):
    node, h_val = input(f"Node {i+1}: ").strip().split()
    heuristics[node] = int(h_val)  
n=int(input("Enter no of edges"))
print("Enter edges in each line(a b)")
for i in range(n):
    node,neighbor,cost=input(f"Enter edge {i+1}").strip().split()
    costn=int(cost)
    graph[node][neighbor]=costn
    graph[neighbor][node]=costn
for node, neighbors in graph.items():
    # Join the ENTIRE list of neighbors into one string
    neighbors_str = ", ".join(neighbors)
    
    # Print the node and its complete list of neighbors
    print(f"{node}: {neighbors_str}")
start=input("Enter start node")
goal=input("Enter goal node")
path,visited=bfs(heuristics,graph,start,goal)
print("Path is",path)
print("route is",visited)
total_cost = 0
# Loop through the path from the first node to the second-to-last node
for i in range(len(path) - 1):
                # Get the cost from the current node to the next one in the path
    edge_cost = graph[path[i]][path[i+1]]
    total_cost += edge_cost
print(f"🗺️ Total Path Cost: {total_cost}")

