import heapq

def ucs(N, A, n0, DICH):
    fringe = []  # Priority queue: (cost, node, path)
    heapq.heappush(fringe, (0, n0, [n0]))
    closed = set()

    while fringe:
        cost, n, path = heapq.heappop(fringe)  # lấy node có chi phí nhỏ nhất
        if n in closed:
            continue

        closed.add(n)
        if n in DICH:
            return f"SOLUTION: {path} với chi phí = {cost}"

        # Duyệt các node kề
        for neighbor, edge_cost in A.get(n, []):
            if neighbor not in closed:
                heapq.heappush(fringe, (cost + edge_cost, neighbor, path + [neighbor]))

    return "No solution"

N = {'A', 'B', 'C', 'D', 'E', 'F'}
A = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 1)],
    'D': [],
    'E': [('F', 1)],
    'F': []
}
n0 = 'A'
DICH = {'F'}

result = ucs(N, A, n0, DICH)
print(result)
# Kết quả: SOLUTION: ['A', 'C', 'F'] với chi phí = 5