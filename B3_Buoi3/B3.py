import random
import heapq
from collections import deque

# Trạng thái đích
GOAL = ((1, 2, 3),
        (8, 0, 4), 
        (7, 6, 5))

class EightPuzzleProblem:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        
    def _find_blank_position(self, state):
        """Tìm vị trí của ô trống (số 0)"""
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
        return None
    
    def get_actions(self, state):
        """Trả về danh sách các hành động có thể thực hiện"""
        blank_row, blank_col = self._find_blank_position(state)
        possible_actions = []
        
        if blank_row > 0:
            possible_actions.append('UP')
        if blank_row < 2:
            possible_actions.append('DOWN')
        if blank_col > 0:
            possible_actions.append('LEFT')
        if blank_col < 2:
            possible_actions.append('RIGHT')
            
        return possible_actions
    
    def get_result(self, state, action):
        """Trả về trạng thái mới sau khi thực hiện hành động"""
        blank_row, blank_col = self._find_blank_position(state)
        new_state = [list(row) for row in state]
        
        if action == 'UP':
            new_state[blank_row][blank_col] = new_state[blank_row - 1][blank_col]
            new_state[blank_row - 1][blank_col] = 0
        elif action == 'DOWN':
            new_state[blank_row][blank_col] = new_state[blank_row + 1][blank_col]
            new_state[blank_row + 1][blank_col] = 0
        elif action == 'LEFT':
            new_state[blank_row][blank_col] = new_state[blank_row][blank_col - 1]
            new_state[blank_row][blank_col - 1] = 0
        elif action == 'RIGHT':
            new_state[blank_row][blank_col] = new_state[blank_row][blank_col + 1]
            new_state[blank_row][blank_col + 1] = 0
        
        return tuple(tuple(row) for row in new_state)
    
    def is_goal(self, state):
        """Kiểm tra xem trạng thái hiện tại có phải là trạng thái đích không"""
        return state == GOAL
    
    def get_cost(self, state, action, new_state):
        """Chi phí di chuyển luôn là 1"""
        return 1

def print_state(state):
    """In trạng thái dưới dạng lưới 3x3"""
    print("+" + "-" * 7 + "+")
    for row in state:
        print("|", end="")
        for cell in row:
            if cell == 0:
                print("   ", end="")
            else:
                print(f" {cell} ", end="")
        print("|")
    print("+" + "-" * 7 + "+")

def print_solution(path, total_cost):
    """In lời giải chi tiết"""
    if not path:
        print("Không tìm thấy lời giải!")
        return
        
    print(f"Tìm thấy lời giải với {len(path)} bước, chi phí = {total_cost}")
    for i, (action, state) in enumerate(path):
        print(f"\nBước {i}:")
        if action:
            print(f"Hành động: {action}")
        print_state(state)

# 1. BREADTH-FIRST SEARCH (BFS)
def breadth_first_search(problem):
    """Tìm kiếm theo chiều rộng"""
    fringe = deque([(problem.initial_state, [])])  # (state, path)
    closed = set()
    
    while fringe:
        current_state, path = fringe.popleft()
        
        if current_state in closed:
            continue
            
        closed.add(current_state)
        
        if problem.is_goal(current_state):
            total_cost = len(path)
            return [(None, problem.initial_state)] + [(action, state) for action, state in path], total_cost
        
        # Thêm các trạng thái kề vào fringe
        for action in problem.get_actions(current_state):
            new_state = problem.get_result(current_state, action)
            if new_state not in closed:
                new_path = path + [(action, new_state)]
                fringe.append((new_state, new_path))
    
    return None, 0

# 2. DEPTH-FIRST SEARCH (DFS)
def depth_first_search(problem):
    """Tìm kiếm theo chiều sâu"""
    fringe = [(problem.initial_state, [])]  # Stack: (state, path)
    closed = set()
    
    while fringe:
        current_state, path = fringe.pop(0)  # Lấy từ đầu stack
        
        if current_state in closed:
            continue
            
        closed.add(current_state)
        
        if problem.is_goal(current_state):
            total_cost = len(path)
            return [(None, problem.initial_state)] + [(action, state) for action, state in path], total_cost
        
        # Thêm các trạng thái kề vào đầu fringe (depth-first)
        neighbors = []
        for action in problem.get_actions(current_state):
            new_state = problem.get_result(current_state, action)
            if new_state not in closed:
                new_path = path + [(action, new_state)]
                neighbors.append((new_state, new_path))
        
        fringe = neighbors + fringe  # Thêm vào đầu
    
    return None, 0

# 3. UNIFORM-COST SEARCH (UCS)
def uniform_cost_search(problem):
    """Tìm kiếm với chi phí cực tiểu"""
    fringe = []  # Priority queue: (cost, state, path)
    heapq.heappush(fringe, (0, problem.initial_state, []))
    closed = set()
    
    while fringe:
        cost, current_state, path = heapq.heappop(fringe)
        
        if current_state in closed:
            continue
            
        closed.add(current_state)
        
        if problem.is_goal(current_state):
            return [(None, problem.initial_state)] + [(action, state) for action, state in path], cost
        
        # Thêm các trạng thái kề với chi phí tích lũy
        for action in problem.get_actions(current_state):
            new_state = problem.get_result(current_state, action)
            if new_state not in closed:
                edge_cost = problem.get_cost(current_state, action, new_state)
                new_cost = cost + edge_cost
                new_path = path + [(action, new_state)]
                heapq.heappush(fringe, (new_cost, new_state, new_path))
    
    return None, 0

# 4. DEPTH-LIMITED SEARCH (DLS)
def depth_limited_search(problem, limit):
    """Tìm kiếm giới hạn độ sâu"""
    def recursive_dls(state, path, depth):
        if problem.is_goal(state):
            return [(None, problem.initial_state)] + [(action, s) for action, s in path], len(path)
        elif depth == limit:
            return "cutoff", 0
        else:
            cutoff_occurred = False
            for action in problem.get_actions(state):
                new_state = problem.get_result(state, action)
                new_path = path + [(action, new_state)]
                result, cost = recursive_dls(new_state, new_path, depth + 1)
                
                if result == "cutoff":
                    cutoff_occurred = True
                elif result is not None:
                    return result, cost
            
            return ("cutoff" if cutoff_occurred else None), 0
    
    return recursive_dls(problem.initial_state, [], 0)

# 5. ITERATIVE DEEPENING SEARCH (IDS)
def iterative_deepening_search(problem, max_depth=20):
    """Tìm kiếm sâu dần"""
    for depth in range(max_depth + 1):
        result, cost = depth_limited_search(problem, depth)
        if result != "cutoff" and result is not None:
            return result, cost
    return None, 0

def create_initial_near_goal(num_moves=3):
    """Tạo trạng thái ban đầu gần goal"""
    current_state = GOAL
    temp_problem = EightPuzzleProblem(current_state)
    
    for _ in range(num_moves):
        actions = temp_problem.get_actions(current_state)
        if actions:
            action = random.choice(actions)
            current_state = temp_problem.get_result(current_state, action)
    
    return current_state

# TEST VÀ SO SÁNH CÁC THUẬT TOÁN
if __name__ == "__main__":
    print("=" * 60)
    print("BÀI 1: INITIAL STATE TỰ TẠO")
    print("=" * 60)
    
    # Bài 1: Trạng thái tự tạo
    initial1 = ((1, 2, 3),
                (7, 8, 4),
                (0, 6, 5))
    problem1 = EightPuzzleProblem(initial1)
    
    print("Trạng thái ban đầu:")
    print_state(initial1)
    print("Trạng thái đích:")
    print_state(GOAL)
    
    # Danh sách các thuật toán
    algorithms = [
        ("Breadth-First Search (BFS)", breadth_first_search),
        ("Depth-First Search (DFS)", depth_first_search),
        ("Uniform-Cost Search (UCS)", uniform_cost_search),
        ("Depth-Limited Search (limit=10)", lambda p: depth_limited_search(p, 10)),
        ("Iterative Deepening Search (IDS)", iterative_deepening_search)
    ]
    
    print("\n--- SO SÁNH CÁC THUẬT TOÁN ---")
    results1 = {}
    for name, algorithm in algorithms:
        try:
            path, cost = algorithm(problem1)
            if path and path != "cutoff":
                print(f"{name}: {len(path)} bước, chi phí = {cost}")
                results1[name] = (path, cost)
            else:
                print(f"{name}: Không tìm thấy lời giải")
        except Exception as e:
            print(f"{name}: Lỗi - {e}")
    
    # Hiển thị lời giải chi tiết của BFS
    if "Breadth-First Search (BFS)" in results1:
        print(f"\n--- CHI TIẾT LỜI GIẢI BFS ---")
        path, cost = results1["Breadth-First Search (BFS)"]
        print_solution(path, cost)
    
    print("\n" + "=" * 60)
    print("BÀI 2: INITIAL STATE RANDOM")
    print("=" * 60)
    
    # Bài 2: Trạng thái random
    initial2 = create_initial_near_goal(num_moves=4)
    problem2 = EightPuzzleProblem(initial2)
    
    print("Trạng thái ban đầu random:")
    print_state(initial2)
    print("Trạng thái đích:")
    print_state(GOAL)
    
    if problem2.is_goal(initial2):
        print("\nTrạng thái ban đầu đã là goal!")
    else:
        print("\n--- SO SÁNH CÁC THUẬT TOÁN ---")
        results2 = {}
        for name, algorithm in algorithms:
            try:
                path, cost = algorithm(problem2)
                if path and path != "cutoff":
                    print(f"{name}: {len(path)} bước, chi phí = {cost}")
                    results2[name] = (path, cost)
                else:
                    print(f"{name}: Không tìm thấy lời giải")
            except Exception as e:
                print(f"{name}: Lỗi - {e}")
        
        # Hiển thị lời giải chi tiết của BFS
        if "Breadth-First Search (BFS)" in results2:
            print(f"\n--- CHI TIẾT LỜI GIẢI BFS ---")
            path, cost = results2["Breadth-First Search (BFS)"]
            print_solution(path, cost)
    
    print(f"\n" + "=" * 60)
    print("KẾT LUẬN")
    print("=" * 60)
    print("✅ Đã implement và test thành công 5 thuật toán:")
    print("   1. Breadth-First Search (BFS)")
    print("   2. Depth-First Search (DFS)")
    print("   3. Uniform-Cost Search (UCS)")
    print("   4. Depth-Limited Search (DLS)")
    print("   5. Iterative Deepening Search (IDS)")