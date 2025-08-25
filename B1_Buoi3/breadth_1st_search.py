from collections import deque

def bfs(N, A, n0, DICH):
    fringe = deque([n0])    # fringe khởi tạo với n0
    closed = set()          # tập đã duyệt

    while fringe:
        n = fringe.popleft()      # lấy phần tử đầu
        closed.add(n)             # đưa vào closed

        if n in DICH:             # nếu là đích
            return f"Solution: {n}"

        # Lấy tất cả nút kề chưa duyệt
        neighbors = [m for m in A[n] if m not in closed and m not in fringe]

        # Nối các nút kề vào fringe
        fringe.extend(neighbors)

    return "No solution"

N = {'A', 'B', 'C', 'D', 'E', 'F'}
A = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
n0 = 'A'
DICH = {'F'}   # Có thể là nhiều đích: {'D', 'F'}

result = bfs(N, A, n0, DICH)
print(result)  # Output: Solution: F