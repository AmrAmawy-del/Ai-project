from pyamaze import maze, agent, COLOR
from queue import Queue as q

def bfs(m, start=None):
    if start is None:
        start = (m.rows, m.cols)

    frontier = q()
    frontier.put(start)
    visited = [start]  # visited list

    bsearch = []  # Tracks all visited cells
    bfspath = {}

    while not frontier.empty():
        current_cell = frontier.get()

        if current_cell == m._goal:
            break

        for d in 'ESNW':
            if m.maze_map[current_cell][d]:  # Check if a path exists in direction d
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
                frontier.put(child_cell)
                bfspath[child_cell] = current_cell  # Map child to parent
                bsearch.append(child_cell)

    fwd_path = {}
    cell = m._goal
    while cell != (m.rows, m.cols):
        fwd_path[bfspath[cell]] = cell
        cell = bfspath[cell]

    return bsearch, bfspath, fwd_path

def main():
    x, y = map(int, input('Enter the size of the maze (x y): ').split())
    m = maze(x, y)
    g_x, g_y = map(int, input('Enter the goal or exit coordinates (x y): ').split())
    m.CreateMaze(g_x, g_y, loopPercent=100)


    bsearch, bfspath, path = bfs(m)
    a = agent(m, footprints=True, color=COLOR.green, shape='square')
    b = agent(m, footprints=True, color=COLOR.yellow, shape='square', filled=False)
    #c = agent(m, g_x, g_y, footprints=True, color=COLOR.cyan, shape='square', filled=True, goal=(m.rows, m.cols))

    m.tracePath({a: bsearch}, delay=100)
    #m.tracePath({c: bfspath})
    m.tracePath({b: path})

    m.run()
if __name__ == "__main__":
    main()