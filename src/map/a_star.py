import numpy as np
from collections import defaultdict


def create_adjacent_list(tile_amount, collision_map=None):
    adjacent_dict = defaultdict(list)
    if collision_map is None:
        collision_map = np.ones(tile_amount**2).reshape(tile_amount, -1)
    node_map = np.arange(tile_amount**2).reshape(tile_amount, -1)

    directions = [[1, 0], [1, 1], [1, -1], [0, 1],
                  [0, -1], [-1, 0], [-1, 1], [-1, -1]]

    for index_x in range(len(node_map)):
        for index_y in range(len(node_map)):
            tile = node_map[index_x][index_y]
            for direction in directions:
                try:
                    if index_x+direction[0] >= 0 and index_y+direction[1] >= 0 and collision_map[index_x+direction[0]][index_y+direction[1]] > 0:
                        adjacent_dict[tile].append(
                            node_map[index_x+direction[0]][index_y+direction[1]])
                except:
                    continue

    return list(adjacent_dict.values()), collision_map


def breadth_first_search(adjacent_list, 
    start, 
    goal, 
    vertices, 
    predecessors_list, 
    distance):

    queue = [] 

    visited = [False for i in range(vertices)]

    for i in range(vertices): 
        distance[i] = 1000000
        predecessors_list[i] = -1

    visited[start] = True 
    distance[start] = 0
    queue.append(start)

    while(len(queue) != 0): 
        u = queue[0]
        queue.pop(0)
        for i in range(len(adjacent_list[u])):
            if visited[adjacent_list[u][i]] == False:
                visited[adjacent_list[u][i]] = True
                distance[adjacent_list[u][i]] = distance[u] + 1
                predecessors_list[adjacent_list[u][i]] = u
                queue.append(adjacent_list[u][i])
                # We stop BFS when we find
                # destination.
                if (adjacent_list[u][i] == goal):
                    return True
        
    return False

def get_shortest_distance(adjacent_list, start, goal, vertices): 

    predecessor_list = [0 for i in range(vertices)]
    distance = [0 for i in range(vertices)]

    if not (breadth_first_search(adjacent_list, start, goal, vertices, predecessor_list, distance)): 
        return None, None

    # vector path stores the shortest path
    path = []
    crawl = goal
    path.append(crawl)
     
    while (predecessor_list[crawl] != -1):
        path.append(predecessor_list[crawl])
        crawl = predecessor_list[crawl]
     
    return path[::-1], distance[goal]

adj_list, _ = create_adjacent_list(4)
