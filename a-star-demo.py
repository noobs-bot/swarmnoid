from astar.demo import make_a_maze, walk_through
from astar.search import AStar

if __name__ == "__main__":
        # Given a map size
        size_x, size_y = 16, 32
        
        # Build a map
        world = make_a_maze(size_x, size_y, density=0.1)
        
        # Set start and end goal
        start = (0, 0)
        goal = (size_x-1, size_y-1)
        
        # Search for path
        path = AStar(world).search(start, goal)

        # Show the path
        walk_through(world, path)