from depth_limited_search import depth_limited_search

def iterative_deepening_search(start, goal, graph, max_depth=100):
    for depth in range(max_depth + 1):  # max_depth để tránh vòng lặp vô tận khi không có lời giải
        result = depth_limited_search(start, goal, graph, depth)
        if result != "cutoff":
            return result
    return "failure"

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': ['G'],
    'G': []
}

result = iterative_deepening_search('A', 'G', graph)
print("Kết quả IDS:", result)