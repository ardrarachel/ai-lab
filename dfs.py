import collections
def dfs(graph,start,goal):
    stack=[(start,[start])]
    visited=[start]
    order=[]
    while stack:
        current,path=stack.pop()
        order.append(current)
        if current==goal:
            print(order)
            return path,visited
        for neighbor in reversed(graph.get(current,[])):
            if neighbor not in visited:
                visited.append(neighbor)
                npath=path+[neighbor]
                stack.append((neighbor,npath))
    return None
graph=collections.defaultdict(list)
n=int(input("Enter no of edges"))
for i in range(n):
    node,neighbor=input(f"enter edge {i+1}:").strip().split()
    graph[node].append(neighbor)
    graph[neighbor].append(node)
for node,neighbor in graph.items():
    print(f"Node {node}: {','.join(neighbor)}")
start=input("Enter start node")
goal=input("Enter goal node")
path,visited=dfs(graph,start,goal)
print("Path is",path)
print("route is",visited)