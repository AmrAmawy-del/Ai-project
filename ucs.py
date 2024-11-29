from pyamaze import maze, agent, COLOR
from queue import PriorityQueue

def ucs(m, start=None):
    """
    Uniform Cost Search (UCS) for solving the maze.
    Args:
        m: Maze object.
        start: Starting position in the maze (optional). Defaults to bottom-right corner.
    Returns:
        visited: List of cells visited during the search.
        cost_so_far: Dictionary mapping each cell to its cumulative cost from the start.
        fwdpath: Dictionary representing the optimal path from start to goal.
    """
    if start is None:
        start = (m.rows, m.cols)

    frontier = PriorityQueue()
    frontier.put((0, start))  # Priority queue holds (cost, cell)
    cost_so_far = {start: 0}  # Cumulative cost for each cell
    visited = []  # List of visited cells
    path = {}  # Maps child cells to parent cells

    while not frontier.empty():
        current_cost, current_cell = frontier.get()
        visited.append(current_cell)

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

                # Assume uniform cost of 1 for each step
                new_cost = current_cost + 1

                if child_cell not in cost_so_far or new_cost < cost_so_far[child_cell]:
                    cost_so_far[child_cell] = new_cost
                    frontier.put((new_cost, child_cell))
                    path[child_cell] = current_cell

    # Reconstruct the forward path from goal to start
    fwdpath = {}
    cell =  m._goal
    while cell != start:
        fwdpath[path[cell]] = cell
        cell = path[cell]

    return visited, cost_so_far, fwdpath

def main():
    # Input maze dimensions and goal coordinates
    x, y = map(int, input('Enter the size of the maze (x y): ').split())
    m = maze(x, y)
    g_x, g_y = map(int, input('Enter the goal or exit coordinates (x y): ').split())
    m.CreateMaze(g_x, g_y, loopPercent=100)

    # Perform UCS
    visited, cost_so_far, fwdpath = ucs(m)
     # Print the total cost to reach the goal
    goal = (g_x, g_y)  # Default goal at top-left corner
    print(f"Total cost to reach the goal {goal}: {cost_so_far.get(goal, 'Not reachable')}")

    # Optional: Print costs for all cells
    print("Costs for each cell:")
    for cell, cost in sorted(cost_so_far.items()):
        print(f"Cell: {cell}, Cost: {cost + 1}")

    # Create agents for visualization
    a = agent(m, footprints=True, color=COLOR.green, shape='square')  # Agent to trace visited cells
    b = agent(m, footprints=True, color=COLOR.yellow, shape='square', filled=False)  # Agent to trace forward path
    ##c = agent(m, g_x, g_y, footprints=True, color=COLOR.cyan, shape='square', filled=True, goal=(m.rows, m.cols))  # Goal agent

    # Trace paths
    m.tracePath({a: visited}, delay=100)
    #m.tracePath({c: cost_so_far})  # Visualize all cells with their cumulative cost
    m.tracePath({b: fwdpath})  # Optimal path

   

    
   

    # Run the maze
    m.run()


if __name__ == "__main__":
    main()
