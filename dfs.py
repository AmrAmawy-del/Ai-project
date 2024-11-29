from pyamaze import maze, agent, COLOR

def dfs(m, start=None):
    """
    Depth-First Search (DFS) for solving the maze.
    Args:
        m: Maze object.
        start: Starting position in the maze (optional). Defaults to bottom-right corner.
    Returns:
        visited: List of cells visited during the search.
        dfspath: Dictionary mapping child cells to parent cells for reconstructing the path.
        fwdpath: Dictionary representing the forward path from start to goal.
    """
    if start is None:
        start = (m.rows, m.cols)

    visited = [start]  # Stack for visited cells
    frontier = [start]  # Stack for cells to explore
    dfspath = {}  # Mapping of child to parent cells

    while frontier:
        current_cell = frontier.pop()

        if current_cell ==  m._goal:  # Goal condition
            break

        for d in 'ESNW':  # Explore all directions
            if m.maze_map[current_cell][d]:  # Check if path exists
                if d == 'E':
                    child_cell = (current_cell[0], current_cell[1] + 1)
                elif d == 'W':
                    child_cell = (current_cell[0], current_cell[1] - 1)
                elif d == 'S':
                    child_cell = (current_cell[0] + 1, current_cell[1])
                elif d == 'N':
                    child_cell = (current_cell[0] - 1, current_cell[1])

                if child_cell in visited:
                    continue

                visited.append(child_cell)
                frontier.append(child_cell)
                dfspath[child_cell] = current_cell

    # Reconstruct the forward path from goal to start
    fwdpath = {}
    cell =  m._goal
    while cell != start:
        fwdpath[dfspath[cell]] = cell
        cell = dfspath[cell]

    return visited, dfspath, fwdpath

def main():
    # Input maze dimensions and goal coordinates
    x, y = map(int, input('Enter the size of the maze (x y): ').split())
    m = maze(x, y)
    g_x, g_y = map(int, input('Enter the goal or exit coordinates (x y): ').split())
    m.CreateMaze(g_x, g_y, loopPercent=100)

    # Perform DFS
    visited, dfspath, fwdpath = dfs(m)

    # Create agents for visualization
    a = agent(m, footprints=True, color=COLOR.green, shape='square')  # Agent to trace visited cells
    b = agent(m, footprints=True, color=COLOR.yellow, shape='square', filled=False)  # Agent to trace forward path
   # c = agent(m, g_x, g_y, footprints=True, color=COLOR.cyan, shape='square', filled=True, goal=(m.rows, m.cols))  # Goal agent

    # Trace paths
    m.tracePath({a: visited}, delay=100)
   # m.tracePath({c: dfspath})
    m.tracePath({b: fwdpath})
    
    

    # Run the maze
    m.run()

if __name__ == "__main__":
    main()
