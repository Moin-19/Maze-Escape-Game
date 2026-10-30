"""Maze Escape Game (PS 61) - console maze with W/A/S/D movement and BFS shortest path."""
from collections import deque

MAZE = [
    list("P..##"),
    list("##.##"),
    list("#...#"),
    list("#.###"),
    list("#...E"),
]
DIRS = {"W": (-1, 0), "A": (0, -1), "S": (1, 0), "D": (0, 1)}


def find(maze, ch):
    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if cell == ch:
                return r, c


def is_open(maze, r, c):
    return 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] != "#"


def print_maze(maze, pos):
    for r, row in enumerate(maze):
        print(" ".join("P" if (r, c) == pos else ("." if cell == "P" else cell)
                       for c, cell in enumerate(row)))
    print(f"Player at (row {pos[0]}, col {pos[1]})")


def shortest_path(maze):
    """BFS from start to exit. Returns list of cells, or None if unreachable."""
    start, end = find(maze, "P"), find(maze, "E")
    prev = {start: None}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        if cur == end:
            path = []
            while cur is not None:
                path.append(cur)
                cur = prev[cur]
            return path[::-1]
        for dr, dc in DIRS.values():
            nxt = (cur[0] + dr, cur[1] + dc)
            if is_open(maze, *nxt) and nxt not in prev:
                prev[nxt] = cur
                queue.append(nxt)
    return None


def play(maze):
    pos, end, moves = find(maze, "P"), find(maze, "E"), 0
    print_maze(maze, pos)
    print("Move with W/A/S/D (several at once allowed, e.g. DDS). Q returns to menu.")
    while True:
        try:
            line = input("Move: ").strip().upper()
        except EOFError:
            return
        for key in line:
            if key == "Q":
                return
            if key not in DIRS:
                print(f"Invalid key '{key}'. Use W, A, S or D only.")
                continue
            r, c = pos[0] + DIRS[key][0], pos[1] + DIRS[key][1]
            if not is_open(maze, r, c):
                where = "outside the maze" if not (
                    0 <= r < len(maze) and 0 <= c < len(maze[0])) else "wall ahead"
                print(f"Cannot move: {where}. Move blocked. Player stays at {pos}.")
                print(f"Moves counted: {moves}")
                continue
            pos, moves = (r, c), moves + 1
            print(f"Player moved to (row {r}, col {c}) | Moves: {moves}")
            print_maze(maze, pos)
            if pos == end:
                print(f"You escaped the maze! Total moves: {moves}")
                return


def show_shortest(maze):
    path = shortest_path(maze)
    if path is None:
        print("No path from start to exit.")
        return
    print("Shortest path:", " -> ".join(map(str, path)))
    print(f"Shortest path length: {len(path) - 1} steps")


def main():
    while True:
        print("\n=== Maze Escape Game ===\n1. Play\n2. Shortest path\n3. Quit")
        try:
            choice = input("Choose an option: ").strip()
        except EOFError:
            break
        if choice == "1":
            play(MAZE)
        elif choice == "2":
            show_shortest(MAZE)
        elif choice == "3":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()