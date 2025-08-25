from typing import List, Tuple, Optional

GOAL = "HELLO WORLD"

# Bật log chi tiết khi cần (True/False)
VERBOSE = False

def make_successors(state: str) -> List[str]:
    """
    Sinh 2 nhánh:
      - Nhánh ĐÚNG: thêm ký tự đúng tiếp theo trong GOAL
      - Nhánh SAI : thêm 'X'
    Dừng sinh nếu state đã đủ độ dài GOAL.
    """
    if len(state) >= len(GOAL):
        return []
    right = GOAL[len(state)]
    return [state + right, state + "X"]


# ---------- DLS: Depth-Limited Search ----------
def dls(start: str, goal: str, limit: int) -> Tuple[Optional[str], Optional[List[str]]]:
    """
    Depth-Limited Search (DFS có giới hạn độ sâu = limit).
    Trả về:
      - (goal, path) nếu tìm thấy
      - ("cutoff", None) nếu bị cắt do chạm limit
      - (None, None) nếu thất bại thật (không còn gì để đi)
    Path là danh sách các state từ start -> goal.
    """
    def rec(state: str, depth: int, path: List[str]):
        if VERBOSE:
            print(f"{'  '*depth}- visit: {repr(state)} (depth={depth})")

        # 1) Goal test
        if state == goal:
            if VERBOSE:
                print(f"{'  '*depth}=> FOUND")
            return state, path  # path đã bao gồm state hiện tại

        # 2) Cắt theo limit
        if depth == limit:
            if VERBOSE:
                print(f"{'  '*depth}(cutoff)")
            return "cutoff", None

        # 3) Mở rộng
        cutoff_hit = False
        for child in make_successors(state):
            # gọi đệ quy, tăng depth, thêm child vào path
            status, cpath = rec(child, depth + 1, path + [child])
            if status == "cutoff":
                cutoff_hit = True
            elif status is not None:
                return status, cpath

        return ("cutoff", None) if cutoff_hit else (None, None)

    return rec(start, 0, [start])


# ---------- IDDFS: Iterative Deepening DFS ----------
def iddfs(start: str, goal: str) -> Tuple[Optional[str], Optional[List[str]], int]:
    """
    Chạy DLS nhiều lần với limit = 0,1,2,... cho tới khi:
      - tìm thấy goal  -> trả về (goal, path, limit_found)
      - thất bại thật  -> (None, None, limit_tried)
    """
    depth = 0
    while True:
        if VERBOSE:
            print(f"\n=== DLS with limit = {depth} ===")
        status, path = dls(start, goal, depth)
        if status != "cutoff":     # tìm thấy (str) hoặc thất bại thật (None)
            return status, path, depth
        depth += 1


# ========== DEMO ==========
if __name__ == "__main__":
    start = ""

    # 1) DLS với limit=5
    status5, path5 = dls(start, GOAL, limit=5)
    print("DLS(limit=5):", status5)

    # 2) DLS với limit=11 (độ dài goal)
    status11, path11 = dls(start, GOAL, limit=len(GOAL))
    print("DLS(limit=11):", status11)
    if path11:
        print("  Steps:", len(path11) - 1)

    # 3) IDDFS
    status, path, used_limit = iddfs(start, GOAL)
    print("\nIDDFS:", status)
    print("  Limit found:", used_limit)
    if path:
        print("  Steps:", len(path) - 1)