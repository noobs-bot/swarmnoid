import heapq
from Grid import generate_matrix_from_image
import cv2
import numpy as np

def get_neighbors(node,grid):
    row, col = node
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []
    grid_size = len(grid) #square shape matrix
    for dx, dy in directions:
        new_row, new_col = row + dx, col + dy
        if 0 <= new_row < grid_size and 0 <= new_col < grid_size and (grid[new_row][new_col] == 'a' or grid[new_row][new_col] == 'b'):
            neighbors.append((new_row, new_col))
    return neighbors

def astar(start, goal,grid):
    heap = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while heap:
        current_cost, current_node = heapq.heappop(heap)

        if current_node == goal:
            break

        for next_node in get_neighbors(current_node,grid):
            new_cost = cost_so_far[current_node] + 1  # Assuming each step costs 1
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal, next_node)
                heapq.heappush(heap, (priority, next_node))
                came_from[next_node] = current_node

    if goal in came_from:
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path
    else:
        return None

def heuristic(node, target):
    return abs(node[0] - target[0]) + abs(node[1] - target[1])


def draw_grid(grid,path=[]):
    grid_size = len(grid)  # Assuming grid is a square matrix

    dark_blue = (50, 25, 125)
    offset_green = (122, 255, 122)
    offset_red = (255, 122, 122)
    red_blue = (255, 0, 255)  # bot for red
    green_blue = (0, 255, 255)  # bot for green
    green = (0, 255, 0)
    red = (255, 0, 0)
    gray = (125, 125, 125)
    black = (0, 0, 0)
    white = (255,255,255)

    cell_size = 30
    height, width = grid_size * cell_size, grid_size * cell_size
    canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

    for i in range(grid_size):
        for j in range(grid_size):
            color = white
            if grid[i][j] == 9:
                color = offset_green
            elif grid[i][j] == 8:
                color = offset_red
            elif grid[i][j] == 6:
                color = red_blue
            elif grid[i][j] == 7:
                color = green_blue
            elif grid[i][j] == 0 or grid[i][j] == 1 or grid[i][j] == 2 or grid[i][j] == 3 or grid[i][j] == 4 or grid[i][j] == 5:
                color = dark_blue
            elif 8 < i < 14 and (j == 2 or j == 3 or j == 4):
                color = green
            elif 8 < j < 14 and (i == 2 or i == 3 or i == 4):
                color = red
            elif grid[i][j] == 'b':
                color = black

            cv2.rectangle(canvas, (j * cell_size, i * cell_size),
            ((j + 1) * cell_size, (i + 1) * cell_size), color, -1)

    #Draws path
    if path:
        for node in path:
            cv2.rectangle(canvas, (node[1] * cell_size, node[0] * cell_size),
            ((node[1] + 1) * cell_size, (node[0] + 1) * cell_size), gray, -1)

    # Draws gridlines
    for i in range(0, width, cell_size):
        cv2.line(canvas, (i, 0), (i, height), black, 1)
    for j in range(0, height, cell_size):
        cv2.line(canvas, (0, j), (width, j), black, 1)

    return canvas

def find_closest_indices(grid, value1, value2):
    matrix_array = np.array(grid)
    start_nodes = np.argwhere(matrix_array == value1)
    end_nodes = np.argwhere(matrix_array == value2)

    if len(start_nodes) > 0 and len(end_nodes) > 0:
        min_distance = float('inf')
        closest_start = None
        closest_end = None

        for s_node in start_nodes:
            for e_node in end_nodes:
                distance = abs(s_node[0] - e_node[0]) + abs(s_node[1] - e_node[1])
                if distance < min_distance:
                    min_distance = distance
                    closest_start = tuple(s_node)
                    closest_end = tuple(e_node)

        return closest_start, closest_end, min_distance

    return None

def position_Bot(bot_id,grid,img_id): #img_id is just for output of process and is not nedded
    final_path = []
    matrix_array = np.array(grid)
    if bot_id == '6':
        closest_start, closest_end, min_distance = find_closest_indices(matrix_array, '6', '9')
        closest_end = (closest_end[0]+1,closest_end[1])
        path = astar(closest_start, closest_end,grid)
        grid[closest_end[0] - 1][closest_end[1]] = 'b'
        grid[closest_start[0]][closest_start[1]] = 'a'
        grid[closest_end[0]][closest_end[1]] = '6'

        matrix_array = np.array(grid)
        # cv2.imshow('1PathGrid{}'.format(img_id),draw_grid(grid,path))
        # cv2.imwrite('images/Dijkstar/bot1/{}PathGrid.png'.format(img_id),draw_grid(grid,path))

        final_path.append({1:path})

    if bot_id == '7':
        closest_start, closest_end, min_distance = find_closest_indices(matrix_array, '7', '8')
        closest_end = (closest_end[0]+1,closest_end[1])
        path = astar(closest_start, closest_end,grid)
        grid[closest_end[0] - 1][closest_end[1]] = 'b'
        grid[closest_start[0]][closest_start[1]] = 'a'
        grid[closest_end[0]][closest_end[1]] = '7'
        
        matrix_array = np.array(grid)
        # cv2.imshow('2PathGrid{}'.format(img_id),draw_grid(grid,path))
        # cv2.imwrite('images/Dijkstar/bot2/{}PathGrid.png'.format(img_id),draw_grid(grid,path))

        final_path.append({2:path})
    final_path = final_path[0] if final_path else {}
    return final_path,grid

def take_home(bot_id,grid,img_id): #img_id is just for output of process and is not nedded
    final_path = []
    matrix_array = np.array(grid)
    if bot_id == '6':
        closest_start, closest_end, min_distance = find_closest_indices(matrix_array, '6', '4')
        closest_end = (closest_end[0] + 2, closest_end[1] + 1)
        path = astar(closest_start, closest_end, grid)
        grid[closest_start[0]][closest_start[1]] = 'a'
        grid[closest_start[0] - 1][closest_start[1]] = 'a'
        grid[closest_end[0]][closest_end[1]] = '6'
        matrix_array = np.array(grid)

        final_path.append({1:path})
        # cv2.imshow('1PushGrid{}'.format(img_id),draw_grid(grid,path))
        # cv2.imwrite('images/Dijkstar/bot1/{}PushGrid.png'.format(img_id),draw_grid(grid,path))

    if bot_id == '7':
        closest_start, closest_end, min_distance = find_closest_indices(matrix_array, '7', '5')
        closest_end = (closest_end[0] +1, closest_end[1] + 2)
        path = astar(closest_start, closest_end, grid)
        grid[closest_start[0]][closest_start[1]] = 'a'
        grid[closest_start[0] - 1][closest_start[1]] = 'a'
        grid[closest_end[0]][closest_end[1]] = '7'
        matrix_array = np.array(grid)

        final_path.append({2:path})
        # cv2.imshow('2PushGrid{}'.format(img_id),draw_grid(grid,path))
        # cv2.imwrite('images/Dijkstar/bot2/{}PushGrid.png'.format(img_id),draw_grid(grid,path))
    final_path = final_path[0] if final_path else {}
    return final_path,grid

def main():

    image_path = 'images\BoardGrid.png'
    grid =generate_matrix_from_image(cv2.imread(image_path))[0]
    matrix_array = np.array(grid)
    img_id=1
    while find_closest_indices(matrix_array, '6', '9') != None or find_closest_indices(matrix_array, '7', '8') != None:
        pick_path = []
        return_path = []
        if find_closest_indices(matrix_array, '6', '9') != None:
            obj_path,grid = position_Bot('6',grid,img_id)
            ret_path,grid = take_home('6',grid,img_id) 
            pick_path.append(obj_path)
            return_path.append(ret_path)

        if find_closest_indices(matrix_array, '7', '8') != None:
            obj_path,grid = position_Bot('7',grid,img_id)
            ret_path,grid = take_home('7',grid,img_id)
            pick_path.append(obj_path)
            return_path.append(ret_path)

        matrix_array = np.array(grid) 
        
        print("{} Pick:".format(img_id),pick_path)
        print("{} HomePath:".format(img_id),return_path)

        img_id += 1

        # something simmilar for 8
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()