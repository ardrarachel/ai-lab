import collections
def bfs(graph,start,goal):
    queue=collections.deque([(start,[start])])
    visited=[start]
    while queue:
        current,path=queue.popleft()
        if current==goal:
            return path,visited
        for neighbor in (graph.get(current,[])):
            if neighbor not in visited:
                visited.append(neighbor)
                npath=path+[neighbor]
                queue.append((neighbor,npath))
    return None
graph=collections.defaultdict(list)
n=int(input("Enter no of edges"))
print("Enter edges in each line(a b)")
for i in range(n):
    node,neighbor=input(f"Enter edge {i+1}").strip().split()
    graph[node].append(neighbor)
    graph[neighbor].append(node)
for node, neighbors in graph.items():
    # Join the ENTIRE list of neighbors into one string
    neighbors_str = ", ".join(neighbors)
    
    # Print the node and its complete list of neighbors
    print(f"{node}: {neighbors_str}")
start=input("Enter start node")
goal=input("Enter goal node")
path,visited=bfs(graph,start,goal)
print("Path is",path)
print("route is",visited)

