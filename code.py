import heapq

class PuzzleState:
    def __init__(self, board, parent=None, move="", depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        # A* priority: distance from start + heuristic
        self.priority = self.depth + self.manhattan_distance()

    def manhattan_distance(self):
        distance = 0
        for r in range(3):
            for c in range(3):
                val = self.board[r][c]
                if val != 0:
                    target_r, target_c = divmod(val - 1, 3)
                    distance += abs(r - target_r) + abs(c - target_c)
        return distance

    def get_neighbors(self):
        neighbors = []
        r, c = next((r, c) for r in range(3) for c in range(3) if self.board[r][c] == 0)
        moves = {"Up": (r-1, c), "Down": (r+1, c), "Left": (r, c-1), "Right": (r, c+1)}
        
        for move_name, (nr, nc) in moves.items():
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_board = [row[:] for row in self.board]
                new_board[r][c], new_board[nr][nc] = new_board[nr][nc], new_board[r][c]
                neighbors.append(PuzzleState(new_board, self, move_name, self.depth + 1))
        return neighbors

    def __lt__(self, other):
        return self.priority < other.priority

def solve(start_board):
    start_state = PuzzleState(start_board)
    frontier = [start_state]
    visited = set()

    while frontier:
        current_state = heapq.heappop(frontier)

        if current_state.board == current_state.goal:
            return backtrack_solution(current_state)

        board_tuple = tuple(tuple(row) for row in current_state.board)
        if board_tuple in visited:
            continue
        visited.add(board_tuple)

        for neighbor in current_state.get_neighbors():
            heapq.heappush(frontier, neighbor)

    return None

def backtrack_solution(state):
    path = []
    while state.parent:
        path.append((state.move, state.board))
        state = state.parent
    return path[::-1]

def display_grid(arr):
    print("-" * 13)
    for row in arr:
        print(f"| {' | '.join(map(str, row))} |")
        print("-" * 13)

import random

def get_solvable_random_board():
    while True:
        # 1. Create a flat list of tiles (0 represents blank)
        tiles = list(range(9))
        random.shuffle(tiles)
        
        # 2. Check Solvability (Inversion Count)
        # An inversion is when a larger number appears before a smaller number
        inversions = 0
        flat_list = [t for t in tiles if t != 0] # exclude the blank
        for i in range(len(flat_list)):
            for j in range(i + 1, len(flat_list)):
                if flat_list[i] > flat_list[j]:
                    inversions += 1
        
        # 3. If inversions are even, it's solvable
        if inversions % 2 == 0:
            # Reshape into 3x3
            return [tiles[0:3], tiles[3:6], tiles[6:9]]

# --- Execution ---
initial_board = get_solvable_random_board()

print("Randomly Generated Solvable Board:")
display_grid(initial_board)

solution = solve(initial_board)

if solution:
    print(f"\nSolved in {len(solution)} moves!")
    # Optionally print only the last 3 moves to avoid flooding the console
    if len(solution) > 5:
        print("... (showing final moves) ...")
        for move, board in solution[-3:]:
            print(f"\nMove: {move}")
            display_grid(board)
    else:
        for move, board in solution:
            print(f"\nMove: {move}")
            display_grid(board)
else:
    print("No solution found.")

