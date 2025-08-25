from collections import deque

GOAL = "HELLO WORLD"

def make_successors(state):
    if len(state) >= len(GOAL): return []
    right = GOAL[len(state)]
    return [state + right, state + "X"]  # 1 đúng + 1 sai

def bfs(start, goal):
    fringe = deque([start])
    seen = {start}                 # đánh dấu NGAY khi enqueue

    while fringe:
        n = fringe.popleft()       # GET_FIRST(fringe)

        if n == goal:
            return f"Solution found: {n}"

        for m in make_successors(n):   # Γ(n)
            if m not in seen:
                fringe.append(m)       # fringe ⊕ Γ(n)
                seen.add(m)            # đánh dấu để khỏi enqueue lại

    return "No solution"

print(bfs("", GOAL))