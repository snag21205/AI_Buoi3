GOAL = "HELLO WORLD"

def make_successors(state: str):
    if len(state) >= len(GOAL):
        return []
    right = GOAL[len(state)]          # nhánh đúng
    return [state + right, state + "X"]  # + 1 nhánh sai

def dls(start: str, goal: str, limit: int):
    """
    Trả về:
      - goal (str) nếu tìm thấy
      - "cutoff" nếu bị cắt do chạm limit
      - None nếu thất bại thực sự (không còn gì để đi)
    """
    def rec(state: str, depth: int):
        if state == goal:
            return state
        if depth == limit:            # cắt ở độ sâu L
            return "cutoff"

        cutoff_hit = False
        for child in make_successors(state):
            res = rec(child, depth + 1)
            if res == "cutoff":
                cutoff_hit = True
            elif res is not None:
                return res
        return "cutoff" if cutoff_hit else None

    return rec(start, 0)

# --- demo ---
print("DLS limit=5 :", dls("", GOAL, 5))     # thường "cutoff" (HELLO WORLD dài 11)
print("DLS limit=11:", dls("", GOAL, 11))    # HELLO WORLD