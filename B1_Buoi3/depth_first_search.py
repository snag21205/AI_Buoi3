def dfs(N, A, n0, DICH):
    fringe = [n0]         # Stack, khởi tạo với node xuất phát
    closed = set()        # Tập đã duyệt

    while fringe:
        n = fringe.pop(0)     # Lấy phần tử đầu tiên của fringe (có thể dùng pop() nếu push ở cuối)
        closed.add(n)
        if n in DICH:
            return f"SOLUTION: {n}"
        # Thêm node kề vào đầu fringe (duyệt sâu trước)
        neighbors = [m for m in A[n] if m not in closed and m not in fringe]
        fringe = neighbors + fringe   # Gamma(n) ⊕ fringe

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
DICH = {'F'}

result = dfs(N, A, n0, DICH)
print(result)   # OUTPUT: SOLUTION: F