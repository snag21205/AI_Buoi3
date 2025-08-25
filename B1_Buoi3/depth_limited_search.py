def depth_limited_search(start, goal, graph, limit):
    def recursive_dls(node, path, depth):
        if node == goal:
            return path + [node]          # Trả về đường đi nếu tới goal
        elif depth == limit:
            return "cutoff"               # Đạt giới hạn thì trả về cutoff
        else:
            cutoff_occurred = False
            for child in graph[node]:
                result = recursive_dls(child, path + [node], depth + 1)
                if result == "cutoff":
                    cutoff_occurred = True
                elif result != "failure":
                    return result         # Nếu tìm được thì trả về luôn
            return "cutoff" if cutoff_occurred else "failure"
    return recursive_dls(start, [], 0)

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': ['G'],
    'G': []
}
result = depth_limited_search('A', 'G', graph, limit=2)
print("Kết quả với limit=2:", result)

result = depth_limited_search('A', 'G', graph, limit=4)
print("Kết quả với limit=4:", result)