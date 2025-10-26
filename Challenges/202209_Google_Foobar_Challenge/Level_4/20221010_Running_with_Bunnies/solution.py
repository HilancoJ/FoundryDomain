def solution(times, times_limit):

    for i in times:
        print i 
    print

    # Initialse the total graph size.
    rows = len(times)

    # Initialse the shortest path graph.
    shortest_path_graph = []

    # Set the initial shortest path graph to infinitely large times.
    for i in range(rows):
        
        # Temporary array will be used to create each row.
        temp = []
        for j in range(rows):
            temp.append(float('Inf'))

        # Append each row to the shortest path graph.
        shortest_path_graph.append(temp)


    # Update shortest path graph 
    for source in range(rows):
        
        shortest_path_graph[source][source] = 0

        for relax in range(rows):
            for i in range(rows):
                for j in range(rows):


                    # print source, relax, i, j, '\t',shortest_path_graph[source][i], times[i][j], shortest_path_graph[source][j]

                    if (shortest_path_graph[source][i] + times[i][j] < shortest_path_graph[source][j]):


                        # print 'into', shortest_path_graph[source][i] + times[i][j]


                        # if (relax == rows - 1):
                        #     return list(range(0, rows - 2))

                        shortest_path_graph[source][j] = shortest_path_graph[source][i] + times[i][j]


    print
    for i in shortest_path_graph:
        print i 
    print 

    # starting point, remaining time, bunnies, path
    path_to_walk = [[0, times_limit, [], [0]]]

    # print path_to_walk

    max_bunnies = []

    while len(path_to_walk) > 0:


        current = path_to_walk.pop()

        print current

        src = current[0]
        remainingTime = current[1]
        bunnies = current[2]
        path = current[3]

        print src, remainingTime, bunnies, path

        if(src > 0 and (src < len(times) - 1) and (src not in bunnies)):
            bunnies.append(src)
            bunnies.sort()

        if (src == len(times) - 1) and (len(bunnies) > len(max_bunnies)):
            max_bunnies = bunnies
            
            if len(max_bunnies) == len(times) - 2:
                return list(range(0, len(times) - 2))

        if len(bunnies) == len(max_bunnies) and sum(bunnies) < sum(max_bunnies):
            max_bunnies = bunnies

        for i in range(0, len(times)):
            if i == src:
                continue
            if remainingTime - shortest_path_graph[src][i] - shortest_path_graph[i][len(times) - 1] < 0:
                continue
            if shortest_path_graph[i][src] + shortest_path_graph[src][i] == 0 and (i in path):
                continue
            new_path = path[:]
            new_path.append(i)
            path_to_walk.append([i, remainingTime - shortest_path_graph[src][i], bunnies[:], new_path])

    return [b - 1 for b in max_bunnies]





print(solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)) # [1, 2]

# print(solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)) # [0, 1]
