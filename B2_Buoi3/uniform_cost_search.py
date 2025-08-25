import heapq

GOAL = "HELLO WORLD"

# ----- CHỌN MỘT TRONG HAI CÁCH TÍNH CHI PHÍ -----
EQUAL_COST = False  # True => mỗi bước cost=1; False => đúng=1, sai X=3

def successors_with_cost(state):
    """Trả về list (next_state, step_cost) theo quy tắc sinh."""
    if len(state) >= len(GOAL):
        return []

    right = GOAL[len(state)]
    if EQUAL_COST:
        # A) cost đều = 1  -> UCS ~ BFS theo độ dài
        return [(state + right, 1), (state + "X", 1)]
    else:
        # B) gán trọng số: đúng = 1, sai = 3 -> UCS ưu tiên nhánh đúng
        return [(state + right, 1), (state + "X", 3)]

def reconstruct(parent, goal):
    path = []
    n = goal
    while n is not None:
        path.append(n)
        n = parent.get(n)
    return list(reversed(path))

def ucs(start, goal):
    # fringe: heap các cặp (g_cost, state)
    fringe = [(0, start)]
    parent = {start: None}
    best_cost = {start: 0}     # cost nhỏ nhất đã biết tới state

    while fringe:
        g, n = heapq.heappop(fringe)          # GET_LOWEST_COST(fringe)

        # Bỏ các bản ghi lỗi thời
        if g != best_cost.get(n, float("inf")):
            continue

        if n == goal:
            path = reconstruct(parent, n)
            return {
                "result": n,
                "cost": g,
                "steps": len(path) - 1,
                "path": path,
            }

        # Nối Γ(n) vào fringe
        for m, c in successors_with_cost(n):
            new_g = g + c
            if new_g < best_cost.get(m, float("inf")):
                best_cost[m] = new_g
                parent[m] = n
                heapq.heappush(fringe, (new_g, m))   # fringe ⊕ Γ(n)

    return None

# ---- RUN ----
ans = ucs("", GOAL)
if ans:
    print("FOUND:", ans["result"])
    print("Total cost:", ans["cost"])
    print("Steps:", ans["steps"])
    print("Path:", " -> ".join(repr(s) for s in ans["path"]))  # bật nếu muốn xem full path
else:
    print("No solution")