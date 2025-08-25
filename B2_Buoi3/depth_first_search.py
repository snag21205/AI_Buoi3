GOAL = "HELLO WORLD"

def make_successors(state):
    if len(state) >= len(GOAL):
        return []
    right = GOAL[len(state)]
    return [state + right, state + "X"]   # 1 nhánh đúng, 1 nhánh sai

def dfs(start, goal):
    fringe = [start]      # fringe là list (hoạt động như stack)
    closed = set()

    while fringe:
        n = fringe.pop(0)   # lấy phần tử đầu (GET_FIRST)
        closed.add(n)

        if n == goal:
            return f"Solution found: {n}"

        # Γ(n) ⊕ fringe  (thêm neighbors vào trước fringe)
        neighbors = [m for m in make_successors(n) if m not in closed and m not in fringe]
        fringe = neighbors + fringe

    return "No solution"

print(dfs("", GOAL))